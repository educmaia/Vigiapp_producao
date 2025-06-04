import time
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta
import threading
from config import config

class RateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.storage_file = Path('logs/rate_limits.json')
        self.storage_file.parent.mkdir(exist_ok=True)
        self._load_storage()
        
        # Configurações padrão
        self.max_attempts = config.SECURITY_LOGIN_ATTEMPTS
        self.window_seconds = 300  # 5 minutos
        self.block_duration = 1800  # 30 minutos
        
    def _load_storage(self):
        """Carrega os dados de rate limiting do arquivo"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    self.storage = json.load(f)
            else:
                self.storage = {
                    'attempts': {},  # {ip: {timestamp: count}}
                    'blocks': {}     # {ip: block_until_timestamp}
                }
                self._save_storage()
        except Exception as e:
            print(f"Erro ao carregar storage de rate limiting: {e}")
            self.storage = {'attempts': {}, 'blocks': {}}
    
    def _save_storage(self):
        """Salva os dados de rate limiting no arquivo"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.storage, f)
        except Exception as e:
            print(f"Erro ao salvar storage de rate limiting: {e}")
    
    def _cleanup_old_attempts(self):
        """Remove tentativas antigas do storage"""
        current_time = time.time()
        for ip in list(self.storage['attempts'].keys()):
            # Remove tentativas fora da janela de tempo
            self.storage['attempts'][ip] = {
                ts: count for ts, count in self.storage['attempts'][ip].items()
                if current_time - float(ts) <= self.window_seconds
            }
            # Remove IPs sem tentativas
            if not self.storage['attempts'][ip]:
                del self.storage['attempts'][ip]
        
        # Remove bloqueios expirados
        self.storage['blocks'] = {
            ip: block_until for ip, block_until in self.storage['blocks'].items()
            if current_time < block_until
        }
    
    def is_blocked(self, ip: str) -> bool:
        """Verifica se um IP está bloqueado"""
        with self.lock:
            self._cleanup_old_attempts()
            return ip in self.storage['blocks'] and time.time() < self.storage['blocks'][ip]
    
    def get_block_time_remaining(self, ip: str) -> Optional[int]:
        """Retorna o tempo restante de bloqueio em segundos"""
        if ip in self.storage['blocks']:
            remaining = self.storage['blocks'][ip] - time.time()
            return max(0, int(remaining))
        return None
    
    def record_attempt(self, ip: str, success: bool = False) -> bool:
        """
        Registra uma tentativa de acesso e retorna True se o IP deve ser bloqueado
        
        Args:
            ip: Endereço IP do cliente
            success: Se a tentativa foi bem-sucedida
            
        Returns:
            bool: True se o IP deve ser bloqueado
        """
        with self.lock:
            current_time = time.time()
            
            # Se o IP está bloqueado, não registra nova tentativa
            if self.is_blocked(ip):
                return True
            
            # Se a tentativa foi bem-sucedida, limpa o histórico
            if success:
                if ip in self.storage['attempts']:
                    del self.storage['attempts'][ip]
                self._save_storage()
                return False
            
            # Registra a tentativa
            if ip not in self.storage['attempts']:
                self.storage['attempts'][ip] = {}
            
            timestamp = str(current_time)
            self.storage['attempts'][ip][timestamp] = self.storage['attempts'][ip].get(timestamp, 0) + 1
            
            # Conta tentativas na janela de tempo
            attempts_in_window = sum(
                count for ts, count in self.storage['attempts'][ip].items()
                if current_time - float(ts) <= self.window_seconds
            )
            
            # Se excedeu o limite, bloqueia o IP
            if attempts_in_window >= self.max_attempts:
                self.storage['blocks'][ip] = current_time + self.block_duration
                self._save_storage()
                return True
            
            self._save_storage()
            return False
    
    def get_attempts_count(self, ip: str) -> int:
        """Retorna o número de tentativas na janela de tempo atual"""
        with self.lock:
            self._cleanup_old_attempts()
            if ip not in self.storage['attempts']:
                return 0
            
            current_time = time.time()
            return sum(
                count for ts, count in self.storage['attempts'][ip].items()
                if current_time - float(ts) <= self.window_seconds
            )

# Instância global do rate limiter
rate_limiter = RateLimiter() 