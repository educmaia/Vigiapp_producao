import os
import datetime
import shutil
import subprocess
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys

# --- Início da Modificação para Tornar o Script Robusto ---

# Adiciona o diretório raiz do projeto ao sys.path
# Isso garante que o script possa ser executado de qualquer lugar e ainda encontrar o pacote vigiapp
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Agora podemos importar a configuração da aplicação
try:
    from vigiapp.config import Config
except ImportError:
    print("Erro: Não foi possível importar a configuração. Certifique-se de que a estrutura do projeto está correta.")
    sys.exit(1)

# --- Fim da Modificação ---


# Configuração do logging
def setup_logging(base_dir):
    log_dir = base_dir / 'vigiapp' / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'backup.log'
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('backup')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging(project_root)

class BackupManager:
    def __init__(self):
        self.base_dir = project_root
        self.backup_dir = self.base_dir / 'vigiapp' / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def get_db_path_from_uri(self, db_uri):
        """Extrai o caminho do arquivo de um URI de banco de dados SQLite."""
        if db_uri.startswith('sqlite:///'):
            # O caminho é absoluto a partir da raiz do sistema de arquivos
            path_str = db_uri[len('sqlite:///'):]
            return Path(path_str)
        return None

    def backup_database(self):
        """Realiza backup do banco de dados SQLite"""
        try:
            db_path = self.get_db_path_from_uri(Config.SQLALCHEMY_DATABASE_URI)
            if not db_path or not db_path.exists():
                logger.error(f"Arquivo do banco de dados não encontrado em {db_path}")
                return False
                
            backup_path = self.backup_dir / f'db_backup_{self.timestamp}.db'
            shutil.copy2(db_path, backup_path)
            
            # Comprimir o backup
            compressed_path = f"{backup_path}.gz"
            subprocess.run(['gzip', str(backup_path)])
            
            logger.info(f"Backup do banco de dados realizado com sucesso: {compressed_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao realizar backup do banco de dados: {str(e)}")
            return False
    
    def backup_uploads(self):
        """Realiza backup da pasta de uploads"""
        try:
            uploads_dir = self.base_dir / 'vigiapp' / 'static' / 'uploads'
            if not uploads_dir.exists():
                logger.info("Pasta de uploads não encontrada, pulando backup.")
                return True
                
            backup_path = self.backup_dir / f'uploads_backup_{self.timestamp}'
            shutil.make_archive(str(backup_path), 'zip', uploads_dir)
            
            logger.info(f"Backup dos uploads realizado com sucesso: {backup_path}.zip")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao realizar backup dos uploads: {str(e)}")
            return False
    
    def cleanup_old_backups(self, days=30):
        """Remove backups antigos"""
        try:
            current_time = datetime.datetime.now()
            for backup_file in self.backup_dir.glob('*'):
                if backup_file.is_file():
                    file_time = datetime.datetime.fromtimestamp(backup_file.stat().st_mtime)
                    age = current_time - file_time
                    
                    if age.days > days:
                        backup_file.unlink()
                        logger.info(f"Backup antigo removido: {backup_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar backups antigos: {str(e)}")
            return False
    
    def run_backup(self):
        """Executa o processo completo de backup"""
        logger.info("Iniciando processo de backup")
        
        success = True
        success &= self.backup_database()
        success &= self.backup_uploads()
        success &= self.cleanup_old_backups()
        
        if success:
            logger.info("Processo de backup concluído com sucesso")
        else:
            logger.error("Processo de backup concluído com erros")
        
        return success

if __name__ == '__main__':
    backup_manager = BackupManager()
    backup_manager.run_backup() 