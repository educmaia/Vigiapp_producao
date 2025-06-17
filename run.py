#!/usr/bin/env python3
import os
import sys

# Adiciona o diretório raiz do projeto ao path para que o pacote 'vigiapp' seja encontrado
# Essencial para executar o script diretamente
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# O load_dotenv é chamado dentro de create_app, não é mais necessário aqui.
# from vigiapp.load_env import load_dotenv
# load_dotenv()

from vigiapp.app import create_app, db
from vigiapp.models import User
from werkzeug.security import generate_password_hash

def init_database(app):
    """Initialize database and create default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@vigiapp.com',
                password='admin123',
                role='admin',
                active=True
            )
            db.session.add(admin)
            db.session.commit()
            print('Default admin user created')

if __name__ == '__main__':
    app = create_app()
    
    # O filtro nl2br já é registrado dentro da factory create_app.
    # Não é mais necessário registrá-lo aqui.
    
    # Initialize database
    with app.app_context():
        db.create_all()
        init_database(app) # init_database já tem um app_context, mas vamos garantir
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)