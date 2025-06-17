import os
import logging
import markupsafe

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect, generate_csrf
from vigiapp.security_headers import security_headers_manager
from vigiapp.email_smtp import EmailSender

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Filtro para converter quebras de linha em <br>
def nl2br(value):
    """Converte quebras de linha em tags <br> para renderização em HTML."""
    if value:
        return markupsafe.Markup(
            markupsafe.escape(value).replace('\\n', markupsafe.Markup('<br>\\n'))
        )
    return ''

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
email_sender = EmailSender()  # Instância global do EmailSender
csrf = CSRFProtect()  # Inicializa a proteção CSRF

def create_app():
    app = Flask(__name__)
    
    # Carrega configurações diretamente do ambiente
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Verifica se a URI do banco foi carregada
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise RuntimeError("DATABASE_URL não foi encontrada no ambiente. A aplicação não pode iniciar.")

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    email_sender.init_app(app)  # Inicializa o EmailSender com o app
    
    # Configura o login manager
    login_manager.login_view = None  # Corrigido para None conforme tipo esperado
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Inicializa headers de segurança
    security_headers_manager.init_app(app)
    
    # Disponibiliza a função csrf_token nos templates
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)
    
    # Registra blueprints
    from vigiapp.routes.auth import auth_bp
    from vigiapp.routes.pessoas import pessoas_bp
    from vigiapp.routes.ingressos import ingressos_bp
    from vigiapp.routes.empresas import empresas_bp
    from vigiapp.routes.entregas import entregas_bp
    from vigiapp.routes.correspondencias import correspondencias_bp
    from vigiapp.routes.ocorrencias import ocorrencias_bp
    from vigiapp.routes.relatorios import relatorios_bp
    from vigiapp.routes.users import users_bp
    
    # Blueprints que já definem seu próprio url_prefix em seus arquivos .py
    app.register_blueprint(auth_bp) # Não tem prefixo
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(ingressos_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(entregas_bp)
    app.register_blueprint(correspondencias_bp)
    app.register_blueprint(ocorrencias_bp)
    app.register_blueprint(relatorios_bp)

    # O blueprint 'users' não define um prefixo, então adicionamos aqui.
    app.register_blueprint(users_bp, url_prefix='/usuarios')
    
    # Registrar filtro nl2br para quebras de linha em templates
    app.jinja_env.filters['nl2br'] = nl2br
    
    return app

# Load user
@login_manager.user_loader
def load_user(user_id):
    from vigiapp.models import User
    return User.query.get(int(user_id))

# A instância 'app' não deve mais ser criada globalmente aqui,
# a factory 'create_app' é o ponto de entrada.
# Deixe o wsgi.py ou run.py criar a instância quando necessário.
# app = create_app()

if __name__ == '__main__':
    app = create_app()
    # O filtro já é registrado na factory, não precisa registrar de novo.
    # Configurar para aceitar conexões externas
    app.run(debug=False, host='0.0.0.0', port=5000)
