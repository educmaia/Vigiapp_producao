"""
Script para realizar migrações no banco de dados
"""
import sys
from app import app, db
from sqlalchemy import inspect, text, Column, Boolean, DateTime

def add_columns_to_user_table():
    """Adiciona novas colunas à tabela user."""
    print("Iniciando migração da tabela user...")
    
    with app.app_context():
        # Verifica se as colunas já existem
        inspector = inspect(db.engine)
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        
        # Adiciona a coluna 'active' se não existir
        if 'active' not in user_columns:
            print("Adicionando coluna 'active' à tabela user...")
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN active BOOLEAN DEFAULT true'))
            db.session.commit()
            print("Coluna 'active' adicionada com sucesso!")
        else:
            print("Coluna 'active' já existe.")
        
        # Adiciona a coluna 'last_login' se não existir
        if 'last_login' not in user_columns:
            print("Adicionando coluna 'last_login' à tabela user...")
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN last_login TIMESTAMP'))
            db.session.commit()
            print("Coluna 'last_login' adicionada com sucesso!")
        else:
            print("Coluna 'last_login' já existe.")
        
    print("Migração concluída com sucesso!")

if __name__ == "__main__":
    add_columns_to_user_table()