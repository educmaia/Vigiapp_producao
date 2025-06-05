# Carregar variáveis de ambiente antes de importar o app
from load_env import load_dotenv
load_dotenv()

from app import create_app
import markupsafe

app = create_app()

# Registrar o filtro nl2br no contexto global
def nl2br(value):
    if value:
        return markupsafe.Markup(
            markupsafe.escape(value).replace('\n', markupsafe.Markup('<br>\n'))
        )
    return ''

app.jinja_env.filters['nl2br'] = nl2br

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
