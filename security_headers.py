from flask import request, current_app
from functools import wraps

class SecurityHeaders:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa os headers de segurança na aplicação"""
        # Configurações padrão
        app.config.setdefault('SECURITY_HEADERS', {
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
        })
        
        # Adiciona os headers em todas as respostas
        @app.after_request
        def add_security_headers(response):
            headers = app.config['SECURITY_HEADERS']
            
            # Adiciona headers de segurança
            for header, value in headers.items():
                response.headers[header] = value
            
            # Remove headers sensíveis
            response.headers.pop('X-Powered-By', None)
            response.headers.pop('Server', None)
            
            return response

def security_headers(f):
    """Decorator para adicionar headers de segurança em rotas específicas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Headers específicos para a rota
        headers = {
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block'
        }
        
        # Adiciona headers à resposta
        for header, value in headers.items():
            response.headers[header] = value
            
        return response
    return decorated_function

# Instância global
security_headers_manager = SecurityHeaders() 