#!/bin/bash

# Script para deploy do VigiApp no GitHub
# Repository: https://github.com/educmaia/VigiApp_

echo "=== Deploy VigiApp para GitHub ==="

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "Erro: Execute este script no diretório raiz do projeto VigiApp"
    exit 1
fi

# Remover lock file se existir
if [ -f ".git/index.lock" ]; then
    echo "Removendo lock file do Git..."
    rm -f .git/index.lock
fi

# Inicializar repositório Git se necessário
if [ ! -d ".git" ]; then
    echo "Inicializando repositório Git..."
    git init
fi

# Configurar remote
echo "Configurando remote do GitHub..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/educmaia/VigiApp_.git

# Verificar remote
echo "Verificando configuração do remote..."
git remote -v

# Adicionar todos os arquivos
echo "Adicionando arquivos ao repositório..."
git add .

# Verificar status
echo "Status do repositório:"
git status

# Fazer commit
echo "Fazendo commit..."
git commit -m "Deploy completo do VigiApp - Sistema de Controle de Acesso

Funcionalidades implementadas:
- Sistema de autenticação com roles (admin/vigilante)
- Gestão completa de pessoas e empresas
- Controle de ingressos e saídas
- Gestão de entregas com upload de imagens
- Sistema de correspondências
- Registro de ocorrências
- Geração de QR Codes
- Relatórios em PDF
- Notificações por email automáticas
- Interface responsiva com Bootstrap
- Validações de formulários
- Controle de permissões baseado em roles
- Suporte a PostgreSQL
- Containerização com Docker
- Documentação completa

Tecnologias utilizadas:
- Flask + SQLAlchemy
- PostgreSQL
- Bootstrap 5
- QR Code generation
- Email notifications
- PDF reporting
- Docker support"

# Configurar branch principal
echo "Configurando branch principal..."
git branch -M main

# Fazer push
echo "Fazendo push para o GitHub..."
echo "ATENÇÃO: Você precisará inserir suas credenciais do GitHub"
git push -u origin main

echo "=== Deploy concluído! ==="
echo "Seu projeto está disponível em: https://github.com/educmaia/VigiApp_"