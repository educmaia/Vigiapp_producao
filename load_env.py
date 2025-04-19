"""
Script para carregar variáveis de ambiente do arquivo .env
"""
import os
from pathlib import Path

def load_dotenv(dotenv_path=None):
    """
    Carrega as variáveis de ambiente de um arquivo .env
    Semelhante à biblioteca python-dotenv, mas simplificado
    
    Args:
        dotenv_path: Caminho para o arquivo .env. Se None, usa o .env no diretório atual
    """
    if dotenv_path is None:
        dotenv_path = Path('.') / '.env'
    
    if not os.path.isfile(dotenv_path):
        print(f"Arquivo .env não encontrado em {dotenv_path}")
        return False
    
    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            
            # Divide a linha em chave e valor
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove aspas no início e fim do valor
            if value and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            
            # Define a variável de ambiente
            os.environ[key] = value
    
    return True

if __name__ == "__main__":
    # Se executado diretamente, carrega as variáveis
    load_dotenv()
    print("Variáveis de ambiente carregadas com sucesso do arquivo .env")