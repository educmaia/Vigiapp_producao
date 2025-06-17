"""
Script WSGI para implantação em produção
"""
# A PRIMEIRA COISA a fazer é carregar as variáveis de ambiente.
# Isso garante que elas estejam disponíveis para todo o resto do código.
from pathlib import Path
import os

# Define o caminho para o .env na raiz do projeto
# __file__ aqui é /var/www/vigiapp/wsgi.py
# .parent é /var/www/vigiapp
# .parent.parent é /var/www
env_path = Path(__file__).parent.parent / '.env'

# Carrega o .env se ele existir
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            os.environ.setdefault(key, value)
    print(f"WSGI: Variáveis carregadas de {env_path}")
else:
    print(f"WSGI: AVISO, {env_path} não encontrado.")


from vigiapp.app import create_app
import markupsafe

app = create_app()

# Registrar o filtro nl2br
def nl2br(value):
    if value:
        return markupsafe.Markup(
            markupsafe.escape(value).replace('\\n', markupsafe.Markup('<br>\\n'))
        )
    return ''

app.jinja_env.filters['nl2br'] = nl2br

if __name__ == "__main__":
    app.run()