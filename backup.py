import os
import datetime
import shutil
import subprocess
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# Configuração do logging
def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'backup.log'
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('backup')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()

class BackupManager:
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def backup_database(self):
        """Realiza backup do banco de dados SQLite"""
        try:
            db_path = Path('controle_portaria.db')
            if not db_path.exists():
                logger.error("Arquivo do banco de dados não encontrado")
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
            uploads_dir = Path('uploads')
            if not uploads_dir.exists():
                logger.info("Pasta de uploads não encontrada")
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