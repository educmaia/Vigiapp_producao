# Instruções para Deploy do VigiApp no GitHub

## Passos para fazer o push para https://github.com/educmaia/VigiApp_

### 1. Preparar o repositório local
```bash
# Inicializar o repositório Git (se ainda não estiver inicializado)
git init

# Adicionar o remote do GitHub
git remote add origin https://github.com/educmaia/VigiApp_.git

# Verificar se o remote foi adicionado corretamente
git remote -v
```

### 2. Configurar o .gitignore (já existe no projeto)
O arquivo .gitignore já está configurado para ignorar:
- Arquivos de ambiente (.env)
- Cache do Python (__pycache__)
- Diretórios de instância
- Arquivos temporários

### 3. Adicionar arquivos ao repositório
```bash
# Adicionar todos os arquivos do projeto
git add .

# Verificar quais arquivos serão commitados
git status
```

### 4. Fazer o commit inicial
```bash
git commit -m "Initial commit: VigiApp - Sistema de Controle de Acesso

- Sistema completo de controle de pessoas e materiais
- Interface web em Flask com PostgreSQL
- Módulos: Pessoas, Empresas, Ingressos, Entregas, Correspondências, Ocorrências
- Sistema de QR Code para identificação
- Controle de acesso baseado em roles (admin/vigilante)
- Notificações por email automáticas
- Interface responsiva com Bootstrap
- Documentação completa incluída"
```

### 5. Fazer o push para o GitHub
```bash
# Push para a branch main
git branch -M main
git push -u origin main
```

### 6. Verificar se precisa de autenticação
Se o repositório for privado ou você não tiver configurado SSH, será necessário:
- Usar Personal Access Token do GitHub
- Ou configurar SSH keys

## Estrutura do Projeto

O VigiApp inclui:

### Arquivos principais:
- `app.py` - Configuração principal do Flask
- `main.py` - Ponto de entrada da aplicação
- `models.py` - Modelos do banco de dados
- `forms.py` - Formulários WTF
- `utils.py` - Funções utilitárias

### Diretórios:
- `routes/` - Blueprints das rotas
- `templates/` - Templates HTML
- `static/` - Arquivos CSS, JS e imagens
- `instance/` - Arquivos de instância (não versionados)

### Documentação:
- `README.md` - Documentação principal
- `CONTRIBUTING.md` - Guia para contribuições
- `DEPLOYMENT.md` - Instruções de deploy
- `LICENSE` - Licença MIT

### Deploy e Containerização:
- `Dockerfile` - Para containerização
- `docker-compose.yml` - Orquestração de containers
- `wsgi.py` - Para deploy em produção
- `requirements.txt` - Dependências Python

## Funcionalidades Implementadas

✅ Sistema de autenticação e autorização
✅ Gestão de pessoas com CPF
✅ Gestão de empresas com CNPJ
✅ Controle de ingressos e saídas
✅ Gestão de entregas com imagens
✅ Controle de correspondências
✅ Registro de ocorrências
✅ Geração de QR Codes
✅ Relatórios em PDF
✅ Notificações por email
✅ Interface responsiva
✅ Validações de formulário
✅ Controle de permissões por role

## Próximos Passos Após Deploy

1. Configurar variáveis de ambiente no GitHub (se usar GitHub Actions)
2. Configurar secrets para produção
3. Documentar processo de desenvolvimento
4. Configurar CI/CD se necessário