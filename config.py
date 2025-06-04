import os
from pathlib import Path
from dotenv import load_dotenv

# Adicionando para que basedir funcione como na edição anterior
basedir = os.path.abspath(os.path.dirname(__file__))

# Carrega variáveis do arquivo .env se existir
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(env_path)

class Config:
    # Configurações de Segurança Originais (exemplo, ajuste conforme o seu original)
    SECURITY_LOGIN_ATTEMPTS = int(os.getenv('SECURITY_LOGIN_ATTEMPTS', '5'))
    SECURITY_FAILED_LOGINS = int(os.getenv('SECURITY_FAILED_LOGINS', '3'))
    SECURITY_SUSPICIOUS_IPS = int(os.getenv('SECURITY_SUSPICIOUS_IPS', '3'))
    SECURITY_FILE_CHANGES = int(os.getenv('SECURITY_FILE_CHANGES', '10'))

    # Configurações de Email Restauradas
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('GMAIL_USERNAME', 'vigiappcpv@gmail.com')
    SMTP_PASSWORD = os.getenv('GMAIL_PASSWORD', '') # Importante: esta senha deve estar no seu .env
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', SMTP_USER) # Usar SMTP_USER como padrão para ALERT_EMAIL
    # Para compatibilidade com Flask-Mail, caso use em outro lugar (originalmente não tinha MAIL_USE_TLS etc direto)
    MAIL_SERVER = SMTP_SERVER
    MAIL_PORT = SMTP_PORT
    MAIL_USERNAME = SMTP_USER
    MAIL_PASSWORD = SMTP_PASSWORD
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ('true', '1', 't')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() in ('true', '1', 't')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', SMTP_USER)

    # Configurações do Banco de Dados (mantendo a sua edição anterior)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'controle_portaria.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações da Aplicação (mantendo a sua edição anterior)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vigiapp-secret-key' # Restaurado para seu valor padrão original
    
    # Configurações de Headers de Segurança (mantendo a sua edição anterior, mas a original era mais completa)
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload', # Original era mais completo
        'Content-Security-Policy': "default-src 'self'; "
                                 "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                                 "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                                 "img-src 'self' data: https://i.ibb.co; "
                                 "font-src 'self' https://cdn.jsdelivr.net; "
                                 "connect-src 'self'; "
                                 "frame-ancestors 'none';", # Restaurado para o original mais completo
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY', # Original era DENY
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin', # Adicionado de volta do original
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()' # Adicionado de volta do original
    }
    
    # As configurações abaixo foram introduzidas por você em uma edição anterior, mantendo-as
    # mas note que SECURITY_PASSWORD_SALT e HASH não são usadas diretamente pelo Flask-Login/Werkzeug da forma como está no código
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'salt-padrao'
    SECURITY_PASSWORD_HASH = 'bcrypt' 
    SECURITY_PASSWORD_LENGTH_MIN = 8

    # Configurações de sessão (mantendo sua edição anterior)
    SESSION_COOKIE_SECURE = False # TEMPORARIAMENTE ALTERADO PARA FALSE PARA TESTE HTTP
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de CSRF (mantendo sua edição anterior)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Configurações de rate limiting (mantendo sua edição anterior)
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Configurações de logging (mantendo sua edição anterior)
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

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