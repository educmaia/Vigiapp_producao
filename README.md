# VigiAPP

Sistema de controle de acesso, vigilância e gestão de pessoas e materiais, fornecendo infraestrutura digital inteligente para rastreamento e comunicação abrangentes.

![Logo do VigiAPP](vigiapp.JPG)

## Descrição

O VigiAPP é um sistema desenvolvido para auxiliar no controle de acesso, monitoramento de visitas, entregas, correspondências e ocorrências em um ambiente institucional. Ele foi criado originalmente como uma aplicação desktop em Python com Tkinter e posteriormente migrado para uma aplicação web utilizando o framework Flask.

## Funcionalidades

- **Gestão de Pessoas**: Cadastro e controle de visitantes com dados pessoais
- **Registro de Ingressos**: Controle de entrada e saída de pessoas com motivo da visita
- **Cadastro de Empresas**: Gerenciamento de empresas parceiras e fornecedores
- **Controle de Entregas**: Registro de entregas com suporte a anexos de imagens
- **Gestão de Correspondências**: Controle de correspondências recebidas e sua destinação
- **Registro de Ocorrências**: Documentação de incidentes com níveis de gravidade
- **Geração de Relatórios**: Relatórios detalhados de todas as atividades
- **Códigos QR**: Geração de QR codes para acesso rápido de informações
- **Notificações por Email**: Envio automático de alertas para eventos importantes

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Banco de Dados**: PostgreSQL
- **Autenticação**: Flask-Login
- **Envio de Email**: Flask-Mail, Gmail SMTP
- **Geração de PDF**: ReportLab
- **Geração de QR Code**: qrcode

## Configuração do Ambiente

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/vigiapp.git
   cd vigiapp
   ```

2. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r dependencies.txt
   ```

4. Configure as variáveis de ambiente:
   ```
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

   Você precisará configurar as seguintes variáveis de ambiente no arquivo `.env`:
   
   **Banco de Dados (PostgreSQL):**
   - `DATABASE_URL`: URL completa de conexão ao PostgreSQL
   - `PGUSER`: Nome de usuário do PostgreSQL
   - `PGPASSWORD`: Senha do PostgreSQL
   - `PGHOST`: Endereço do servidor PostgreSQL
   - `PGPORT`: Porta do PostgreSQL (normalmente 5432)
   - `PGDATABASE`: Nome do banco de dados

   **Email (Gmail SMTP):**
   - `GMAIL_PASSWORD`: Senha de aplicativo do Gmail para envio de emails
   
   **Segurança:**
   - `SECRET_KEY`: Chave secreta para proteção das sessões e tokens

   **Serviços Opcionais:**
   - `MAILERSEND_API_KEY`: Chave de API do MailerSend (opcional)
   - `SENDGRID_API_KEY`: Chave de API do SendGrid (opcional)
   - `TWILIO_ACCOUNT_SID`: ID da conta Twilio para SMS (opcional)
   - `TWILIO_AUTH_TOKEN`: Token de autenticação Twilio (opcional)
   - `TWILIO_PHONE_NUMBER`: Número de telefone Twilio para enviar SMS (opcional)

5. Execute o aplicativo:
   ```
   python main.py
   ```

## Estrutura do Projeto

```
vigiapp/
├── routes/                  # Rotas e controladores do Flask
├── static/                  # Arquivos estáticos (CSS, JS, imagens)
├── templates/               # Templates HTML
├── app.py                   # Configuração principal da aplicação
├── main.py                  # Ponto de entrada da aplicação para desenvolvimento
├── wsgi.py                  # Ponto de entrada para produção (WSGI)
├── models.py                # Modelos do banco de dados
├── forms.py                 # Formulários wtforms
├── email_smtp.py            # Configuração de envio de email
├── qr_code.py               # Utilitários para geração de QR codes
├── utils.py                 # Funções utilitárias
├── dependencies.txt         # Lista de dependências
├── .env.example             # Exemplo de variáveis de ambiente
├── Dockerfile               # Configuração para build de imagem Docker
├── docker-compose.yml       # Configuração para deploy com Docker Compose
├── DEPLOYMENT.md            # Instruções detalhadas de implantação
├── CONTRIBUTING.md          # Guia para contribuidores
└── LICENSE                  # Licença MIT
```

Para instruções detalhadas sobre implantação em diferentes ambientes, consulte o arquivo [DEPLOYMENT.md](DEPLOYMENT.md).

## Contribuindo

Para contribuir com o VigiAPP:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Consulte o [Guia de Contribuição](CONTRIBUTING.md) para obter informações detalhadas sobre como contribuir com o projeto, incluindo padrões de código, processo de pull request e outros requisitos.

## Autor

Eduardo C. Maia - [GitHub](https://github.com/educmaia)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Agradecimentos

- IFSP Campus Capivari
- Departamento de Vigilância
- Equipe de desenvolvimento