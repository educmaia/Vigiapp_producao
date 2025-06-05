"""
Script WSGI para implantação em produção
"""
from load_env import load_dotenv
load_dotenv()

from app import create_app
import markupsafe

app = create_app()

# Registrar o filtro nl2br
def nl2br(value):
    if value:
        return markupsafe.Markup(
            markupsafe.escape(value).replace('\n', markupsafe.Markup('<br>\n'))
        )
    return ''

app.jinja_env.filters['nl2br'] = nl2br

if __name__ == "__main__":
    app.run()