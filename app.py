import os
import logging
import markupsafe

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from email_smtp import EmailSender
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import config
from security_headers import security_headers_manager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Filtro para converter quebras de linha em <br>
def nl2br(value):
    if value:
        return markupsafe.Markup(
            markupsafe.escape(value).replace('\n', markupsafe.Markup('<br>\n'))
        )
    return ''

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
email_sender = EmailSender()  # Instância global do EmailSender
csrf = CSRFProtect()  # Inicializa a proteção CSRF

def create_app():
    app = Flask(__name__)
    
    # Carrega configurações
    app.config.from_object(config)
    
    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configura o login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Inicializa headers de segurança
    security_headers_manager.init_app(app)
    
    # Disponibiliza a função csrf_token nos templates
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)
    
    # Registra blueprints
    from routes.auth import auth_bp
    from routes.pessoas import pessoas_bp
    from routes.ingressos import ingressos_bp
    from routes.empresas import empresas_bp
    from routes.entregas import entregas_bp
    from routes.correspondencias import correspondencias_bp
    from routes.ocorrencias import ocorrencias_bp
    from routes.relatorios import relatorios_bp
    from routes.qr_routes import qr_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(ingressos_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(entregas_bp)
    app.register_blueprint(correspondencias_bp)
    app.register_blueprint(ocorrencias_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(users_bp, url_prefix='/usuarios')
    
    return app

# Load user
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    
    # Registrar o filtro nl2br
    app.jinja_env.filters['nl2br'] = nl2br
    
    # Configurar para aceitar conexões externas
    app.run(debug=False, host='0.0.0.0', port=5000)
