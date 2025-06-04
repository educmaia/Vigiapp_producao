import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env se existir
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(env_path)

class Config:
    # Configurações de Segurança
    SECURITY_LOGIN_ATTEMPTS = int(os.getenv('SECURITY_LOGIN_ATTEMPTS', '5'))
    SECURITY_FAILED_LOGINS = int(os.getenv('SECURITY_FAILED_LOGINS', '3'))
    SECURITY_SUSPICIOUS_IPS = int(os.getenv('SECURITY_SUSPICIOUS_IPS', '3'))
    SECURITY_FILE_CHANGES = int(os.getenv('SECURITY_FILE_CHANGES', '10'))
    
    # Configurações de Email (usando as mesmas do sistema existente)
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = os.getenv('GMAIL_USERNAME', 'vigiappcpv@gmail.com')
    SMTP_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
    ALERT_EMAIL = os.getenv('GMAIL_USERNAME', 'vigiappcpv@gmail.com')
    
    # Configurações do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///controle_portaria.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações da Aplicação
    SECRET_KEY = os.getenv('SECRET_KEY', 'vigiapp-secret-key')
    
    # Configurações de Headers de Segurança
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'Content-Security-Policy': "default-src 'self'; "
                                 "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                                 "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                                 "img-src 'self' data: https://i.ibb.co; "
                                 "font-src 'self' https://cdn.jsdelivr.net; "
                                 "connect-src 'self'; "
                                 "frame-ancestors 'none';",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }
    
    @classmethod
    def validate_email_config(cls):
        """Valida se as configurações de email estão completas"""
        if not cls.SMTP_PASSWORD:
            print("AVISO: GMAIL_PASSWORD não encontrada. Sistema de email desabilitado.")
            return False
        return True
    
    @classmethod
    def get_email_config(cls):
        """Retorna as configurações de email em um dicionário"""
        return {
            'server': cls.SMTP_SERVER,
            'port': cls.SMTP_PORT,
            'user': cls.SMTP_USER,
            'password': cls.SMTP_PASSWORD,
            'alert_email': cls.ALERT_EMAIL
        }
    
    @classmethod
    def get_security_config(cls):
        """Retorna as configurações de segurança em um dicionário"""
        return {
            'login_attempts': cls.SECURITY_LOGIN_ATTEMPTS,
            'failed_logins': cls.SECURITY_FAILED_LOGINS,
            'suspicious_ips': cls.SECURITY_SUSPICIOUS_IPS,
            'file_changes': cls.SECURITY_FILE_CHANGES
        }

# Instância de configuração
config = Config() 