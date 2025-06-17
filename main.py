import os
import sys

# Adiciona o diretório raiz do projeto ao path para que o pacote 'vigiapp' seja encontrado
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from vigiapp.app import create_app

# A factory 'create_app' já carrega o .env, inicializa o db e registra os filtros
app = create_app()

if __name__ == '__main__':
    # O modo debug recarrega o servidor a cada alteração de código.
    # Ideal para desenvolvimento.
    app.run(host='0.0.0.0', port=5000, debug=True)
