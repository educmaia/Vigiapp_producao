import os
import subprocess
from pathlib import Path

def setup_backup_cron():
    # Obtém o caminho absoluto do diretório atual
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Cria o comando para o cron
    python_path = subprocess.check_output(['which', 'python3']).decode().strip()
    backup_script = current_dir / 'backup.py'
    
    # Comando que será executado pelo cron
    cron_command = f"0 2 * * * cd {current_dir} && {python_path} {backup_script} >> {current_dir}/logs/cron.log 2>&1\n"
    
    # Adiciona o comando ao crontab
    try:
        # Obtém o crontab atual
        current_crontab = subprocess.check_output(['crontab', '-l']).decode()
        
        # Verifica se o comando já existe
        if cron_command.strip() not in current_crontab:
            # Adiciona o novo comando
            new_crontab = current_crontab.rstrip() + '\n' + cron_command
            
            # Atualiza o crontab
            subprocess.run(['crontab', '-'], input=new_crontab.encode())
            print("Cron job configurado com sucesso!")
        else:
            print("Cron job já existe!")
            
    except subprocess.CalledProcessError:
        # Se não houver crontab, cria um novo
        subprocess.run(['crontab', '-'], input=cron_command.encode())
        print("Cron job configurado com sucesso!")

if __name__ == '__main__':
    setup_backup_cron() 