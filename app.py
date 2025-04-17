import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create and configure the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vigiapp-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///controle_portaria.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

# Import models and create tables
with app.app_context():
    from models import User
    db.create_all()

    # Create default admin user if it doesn't exist
    from werkzeug.security import generate_password_hash
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@vigiapp.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        app.logger.info('Default admin user created')

# Register blueprints
from routes.auth import auth_bp
from routes.pessoas import pessoas_bp
from routes.ingressos import ingressos_bp
from routes.empresas import empresas_bp
from routes.entregas import entregas_bp
from routes.correspondencias import correspondencias_bp
from routes.ocorrencias import ocorrencias_bp
from routes.relatorios import relatorios_bp

app.register_blueprint(auth_bp)
app.register_blueprint(pessoas_bp)
app.register_blueprint(ingressos_bp)
app.register_blueprint(empresas_bp)
app.register_blueprint(entregas_bp)
app.register_blueprint(correspondencias_bp)
app.register_blueprint(ocorrencias_bp)
app.register_blueprint(relatorios_bp)

# Load user
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
