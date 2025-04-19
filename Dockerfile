FROM python:3.11-slim

WORKDIR /app

# Instalação de dependências
COPY dependencies.txt .
RUN pip install --no-cache-dir -r dependencies.txt

# Cópia dos arquivos do projeto
COPY . .

# Configuração das variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Exposição da porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]