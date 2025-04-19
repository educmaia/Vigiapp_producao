# Instruções de Implantação do VigiAPP

Este documento fornece instruções detalhadas para implantar o VigiAPP em diferentes ambientes.

## Implantação em Ambiente de Desenvolvimento

Para executar o VigiAPP em ambiente de desenvolvimento:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/vigiapp.git
   cd vigiapp
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r dependencies.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Execute o aplicativo em modo de desenvolvimento:
   ```bash
   python main.py
   ```

## Implantação em Ambiente de Produção

Para implantar o VigiAPP em um servidor de produção:

### Opção 1: Usando Gunicorn (recomendado)

1. Instale o Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Inicie o servidor:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

3. Configure um proxy reverso (Nginx ou Apache) para encaminhar as solicitações para o Gunicorn.

### Opção 2: Usando Docker

1. Construa a imagem Docker:
   ```bash
   docker build -t vigiapp .
   ```

2. Execute o contêiner:
   ```bash
   docker run -d -p 5000:5000 --name vigiapp --env-file .env vigiapp
   ```

## Configuração do Banco de Dados

### Criação do Banco de Dados PostgreSQL

1. Instale o PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql postgresql-server
   ```

2. Crie um usuário e banco de dados:
   ```bash
   sudo -u postgres psql
   
   CREATE USER vigiapp_user WITH PASSWORD 'sua_senha_segura';
   CREATE DATABASE vigiapp OWNER vigiapp_user;
   GRANT ALL PRIVILEGES ON DATABASE vigiapp TO vigiapp_user;
   \q
   ```

3. Configure a conexão no arquivo `.env`:
   ```
   DATABASE_URL=postgresql://vigiapp_user:sua_senha_segura@localhost:5432/vigiapp
   ```

## Configuração de Email

### Configuração do Gmail SMTP

1. Configure uma conta do Gmail com [Senha de Aplicativo](https://support.google.com/accounts/answer/185833?hl=pt-BR)
2. Adicione as credenciais ao arquivo `.env`:
   ```
   GMAIL_PASSWORD=sua_senha_de_aplicativo_aqui
   ```

## Servidor Web Nginx (Produção)

Configure o Nginx como proxy reverso para o Gunicorn:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Configuração do Systemd (Linux)

Crie um arquivo de serviço para manter o aplicativo em execução:

```ini
[Unit]
Description=VigiAPP - Sistema de Controle de Acesso
After=network.target

[Service]
User=seu_usuario
WorkingDirectory=/caminho/para/vigiapp
ExecStart=/caminho/para/vigiapp/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Salve como `/etc/systemd/system/vigiapp.service` e ative com:

```bash
sudo systemctl enable vigiapp
sudo systemctl start vigiapp
```

## Verificação da Implantação

1. Verifique o status do serviço:
   ```bash
   # Se usando systemd
   sudo systemctl status vigiapp
   
   # Se usando Docker
   docker ps -a
   ```

2. Verifique os logs para problemas:
   ```bash
   # Se usando systemd
   sudo journalctl -u vigiapp
   
   # Se usando Docker
   docker logs vigiapp
   ```

3. Teste o acesso à aplicação navegando para `http://seu-servidor:5000` ou `https://seu-dominio.com`