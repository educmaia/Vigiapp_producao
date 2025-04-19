"""
Script WSGI para implantação em produção
"""
from load_env import load_dotenv
load_dotenv()

from app import app

if __name__ == "__main__":
    app.run()