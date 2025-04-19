# Carregar variáveis de ambiente antes de importar o app
from load_env import load_dotenv
load_dotenv()

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
