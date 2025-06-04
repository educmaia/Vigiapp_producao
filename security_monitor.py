import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from pathlib import Path
import json
from typing import Dict, List, Optional
from config import config

class SecurityMonitor:
    def __init__(self):
        self.logger = self._setup_logger()
        self.alert_thresholds = config.get_security_config()
        self.alert_history_file = Path('logs/security_alerts.json')
        self._load_alert_history()
        
    def _setup_logger(self) -> logging.Logger:
        """Configura o logger para o monitor de segurança"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger('security_monitor')
        logger.setLevel(logging.INFO)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_dir / 'security.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
        
        return logger
    
    def _load_alert_history(self):
        """Carrega o histórico de alertas"""
        if self.alert_history_file.exists():
            with open(self.alert_history_file, 'r') as f:
                self.alert_history = json.load(f)
        else:
            self.alert_history = {
                'login_attempts': {},
                'failed_logins': {},
                'suspicious_ips': {},
                'file_changes': {}
            }
    
    def _save_alert_history(self):
        """Salva o histórico de alertas"""
        with open(self.alert_history_file, 'w') as f:
            json.dump(self.alert_history, f, indent=4)
    
    def _send_email_alert(self, subject: str, message: str):
        """Envia alerta por email"""
        try:
            # Verificar configurações de email
            if not config.validate_email_config():
                self.logger.error("Configurações de email incompletas")
                return
            
            email_config = config.get_email_config()
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = email_config['user']
            msg['To'] = email_config['alert_email']
            msg['Subject'] = f"[VigiAPP] Alerta de Segurança: {subject}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Enviar email
            with smtplib.SMTP(email_config['server'], email_config['port']) as server:
                server.starttls()
                server.login(email_config['user'], email_config['password'])
                server.send_message(msg)
                
            self.logger.info(f"Alerta enviado por email: {subject}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar email de alerta: {str(e)}")
    
    def monitor_login_attempt(self, username: str, ip_address: str, success: bool):
        """Monitora tentativas de login"""
        current_time = datetime.now().isoformat()
        
        # Registrar tentativa
        if username not in self.alert_history['login_attempts']:
            self.alert_history['login_attempts'][username] = []
        
        self.alert_history['login_attempts'][username].append({
            'timestamp': current_time,
            'ip': ip_address,
            'success': success
        })
        
        # Limpar tentativas antigas (mais de 1 hora)
        self.alert_history['login_attempts'][username] = [
            attempt for attempt in self.alert_history['login_attempts'][username]
            if (datetime.now() - datetime.fromisoformat(attempt['timestamp'])).seconds < 3600
        ]
        
        # Verificar se excedeu o limite
        if len(self.alert_history['login_attempts'][username]) >= self.alert_thresholds['login_attempts']:
            message = f"""
            Alerta de Segurança - Múltiplas Tentativas de Login
            
            Usuário: {username}
            IP: {ip_address}
            Número de tentativas: {len(self.alert_history['login_attempts'][username])}
            Última tentativa: {current_time}
            
            Recomendação: Verificar se há tentativa de acesso não autorizado.
            """
            self._send_email_alert("Múltiplas Tentativas de Login", message)
            self.logger.warning(f"Múltiplas tentativas de login detectadas para usuário {username}")
        
        self._save_alert_history()
    
    def monitor_file_changes(self, file_path: str, change_type: str, user: str):
        """Monitora alterações em arquivos sensíveis"""
        current_time = datetime.now().isoformat()
        
        # Registrar alteração
        if file_path not in self.alert_history['file_changes']:
            self.alert_history['file_changes'][file_path] = []
        
        self.alert_history['file_changes'][file_path].append({
            'timestamp': current_time,
            'type': change_type,
            'user': user
        })
        
        # Limpar alterações antigas (mais de 24 horas)
        self.alert_history['file_changes'][file_path] = [
            change for change in self.alert_history['file_changes'][file_path]
            if (datetime.now() - datetime.fromisoformat(change['timestamp'])).seconds < 86400
        ]
        
        # Verificar se excedeu o limite
        if len(self.alert_history['file_changes'][file_path]) >= self.alert_thresholds['file_changes']:
            message = f"""
            Alerta de Segurança - Múltiplas Alterações em Arquivo
            
            Arquivo: {file_path}
            Usuário: {user}
            Número de alterações: {len(self.alert_history['file_changes'][file_path])}
            Última alteração: {current_time}
            
            Recomendação: Verificar se as alterações são legítimas.
            """
            self._send_email_alert("Múltiplas Alterações em Arquivo", message)
            self.logger.warning(f"Múltiplas alterações detectadas no arquivo {file_path}")
        
        self._save_alert_history()
    
    def monitor_suspicious_ip(self, ip_address: str, reason: str):
        """Monitora IPs suspeitos"""
        current_time = datetime.now().isoformat()
        
        # Registrar IP suspeito
        if ip_address not in self.alert_history['suspicious_ips']:
            self.alert_history['suspicious_ips'][ip_address] = []
        
        self.alert_history['suspicious_ips'][ip_address].append({
            'timestamp': current_time,
            'reason': reason
        })
        
        # Limpar registros antigos (mais de 24 horas)
        self.alert_history['suspicious_ips'][ip_address] = [
            record for record in self.alert_history['suspicious_ips'][ip_address]
            if (datetime.now() - datetime.fromisoformat(record['timestamp'])).seconds < 86400
        ]
        
        # Verificar se excedeu o limite
        if len(self.alert_history['suspicious_ips'][ip_address]) >= self.alert_thresholds['suspicious_ips']:
            message = f"""
            Alerta de Segurança - IP Suspeito
            
            IP: {ip_address}
            Motivo: {reason}
            Número de ocorrências: {len(self.alert_history['suspicious_ips'][ip_address])}
            Última ocorrência: {current_time}
            
            Recomendação: Considerar bloquear este IP se o comportamento persistir.
            """
            self._send_email_alert("IP Suspeito Detectado", message)
            self.logger.warning(f"IP suspeito detectado: {ip_address}")
        
        self._save_alert_history()

# Instância global do monitor de segurança
security_monitor = SecurityMonitor() 