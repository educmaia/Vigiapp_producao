import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Importa o EmailSender
from email_smtp import EmailSender

class Base(DeclarativeBase):
    pass

# Inicializa as extensões
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
email_sender = EmailSender()  # Instância global do EmailSender

def create_app():
    # Cria e configura o aplicativo
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_not_secure'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///instance/vigiapp.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Outras configurações...
    )
    
    # Configura o login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    # Configura o banco de dados
    db.init_app(app)
    
    # Configura o email sender
    email_sender.init_app(app)
    
    # Importa e registra blueprints
    with app.app_context():
        # Importa modelos
        from . import models
        
        # Cria as tabelas
        db.create_all()
        
        # Registra os blueprints
        from .routes import auth, main, pessoas, ingressos, empresas, correspondencias, ocorrencias, relatorios, entregas, qr_routes
        
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(pessoas.bp)
        app.register_blueprint(ingressos.bp)
        app.register_blueprint(empresas.bp)
        app.register_blueprint(correspondencias.bp)
        app.register_blueprint(ocorrencias.bp)
        app.register_blueprint(relatorios.bp)
        app.register_blueprint(entregas.bp)
        app.register_blueprint(qr_routes.bp)
        
        # Configura a página inicial
        app.add_url_rule('/', endpoint='index')
        
    return app