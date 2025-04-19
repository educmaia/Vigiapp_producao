"""
Script para realizar migrações no banco de dados
"""
from app import app, db
from sqlalchemy import inspect, text

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

def update_enterprise_relationships():
    """Atualiza as relações entre Empresa e Entrega para suporte a CASCADE."""
    print("Iniciando migração das relações entre Empresa e Entrega...")
    
    with app.app_context():
        try:
            # Primeiro adicionar um novo constraint para a chave estrangeira com CASCADE
            # Para isso, precisamos remover o constraint existente e criar um novo
            
            # Verificar se a constraint existe
            inspector = inspect(db.engine)
            foreign_keys = inspector.get_foreign_keys('entregas')
            constraint_name = None
            
            for fk in foreign_keys:
                if 'cnpj' in fk['constrained_columns'] and fk['referred_table'] == 'empresas':
                    constraint_name = fk['name']
                    break
            
            if constraint_name:
                print(f"Removendo constraint: {constraint_name}...")
                # Remover a constraint existente
                db.session.execute(
                    text(f'ALTER TABLE entregas DROP CONSTRAINT IF EXISTS {constraint_name}')
                )
                db.session.commit()
                
                # Criar a nova constraint com CASCADE
                print("Criando nova constraint com CASCADE...")
                db.session.execute(
                    text('ALTER TABLE entregas ADD CONSTRAINT fk_entregas_empresas ' +
                         'FOREIGN KEY (cnpj) REFERENCES empresas(cnpj) ON DELETE CASCADE')
                )
                db.session.commit()
                print("Constraint atualizada com sucesso!")
            else:
                print("Nenhuma constraint entre entregas e empresas encontrada, criando nova...")
                # Criar a nova constraint com CASCADE
                db.session.execute(
                    text('ALTER TABLE entregas ADD CONSTRAINT fk_entregas_empresas ' +
                         'FOREIGN KEY (cnpj) REFERENCES empresas(cnpj) ON DELETE CASCADE')
                )
                db.session.commit()
                print("Nova constraint criada com sucesso!")
                
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar relações: {str(e)}")
            raise
    
    print("Migração das relações concluída com sucesso!")

if __name__ == "__main__":
    add_columns_to_user_table()
    update_enterprise_relationships()