# Guia para Deploy no GitHub

## Como fazer o push do VigiApp para https://github.com/educmaia/VigiApp_

### Opção 1: Download e Upload Manual

1. **Baixar o projeto do Replit:**
   - Clique em "Download as ZIP" no menu do Replit
   - Extraia o arquivo ZIP em seu computador

2. **Preparar o repositório no GitHub:**
   - Acesse https://github.com/educmaia/VigiApp_
   - Clone o repositório em seu computador:
   ```bash
   git clone https://github.com/educmaia/VigiApp_.git
   cd VigiApp_
   ```

3. **Copiar arquivos:**
   - Copie todos os arquivos do projeto extraído para a pasta do repositório
   - Mantenha a pasta `.git` existente

4. **Fazer o commit e push:**
   ```bash
   git add .
   git commit -m "Deploy completo do VigiApp - Sistema de Controle de Acesso"
   git push origin main
   ```

### Opção 2: Conectar Replit ao GitHub

1. **No Replit:**
   - Vá em "Tools" > "Git"
   - Configure suas credenciais do GitHub
   - Conecte ao repositório https://github.com/educmaia/VigiApp_

2. **Fazer o push:**
   - Use a interface Git do Replit para fazer commit e push

### Arquivos Importantes Incluídos

- Sistema completo de controle de acesso
- Documentação (README.md, CONTRIBUTING.md, DEPLOYMENT.md)
- Configuração Docker (Dockerfile, docker-compose.yml)
- Configuração de produção (wsgi.py)
- Dependências (pyproject.toml)
- Licença MIT

### Estrutura do Projeto

```
VigiApp/
├── app.py                 # Configuração Flask
├── main.py               # Ponto de entrada
├── models.py             # Modelos do banco
├── forms.py              # Formulários WTF
├── utils.py              # Funções utilitárias
├── routes/               # Blueprints
├── templates/            # Templates HTML
├── static/               # CSS, JS, imagens
├── README.md             # Documentação
├── Dockerfile            # Container Docker
├── docker-compose.yml    # Orquestração
└── requirements.txt      # Dependências
```

### Funcionalidades do Sistema

- Autenticação com roles (admin/vigilante)
- Gestão de pessoas e empresas
- Controle de ingressos/saídas
- Sistema de entregas com imagens
- Correspondências e ocorrências
- QR Codes automáticos
- Relatórios PDF
- Notificações por email
- Interface responsiva

O projeto está pronto para deploy e uso em produção.