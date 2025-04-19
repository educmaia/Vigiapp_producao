# Guia de Contribuição para o VigiAPP

Obrigado pelo interesse em contribuir com o VigiAPP! Este documento fornece diretrizes para contribuir com nosso projeto.

## Fluxo de Trabalho para Contribuições

1. Faça um fork do repositório
2. Clone seu fork: `git clone https://github.com/seu-usuario/vigiapp.git`
3. Crie uma branch para sua feature: `git checkout -b feature/nome-da-feature`
4. Implemente suas mudanças
5. Commit das alterações: `git commit -m 'Adiciona nova feature'`
6. Push para o GitHub: `git push origin feature/nome-da-feature`
7. Crie um Pull Request para o repositório original

## Configuração do Ambiente de Desenvolvimento

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r dependencies.txt
   ```

3. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

4. Execute as migrações do banco de dados:
   ```bash
   python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"
   ```

5. Inicie o servidor de desenvolvimento:
   ```bash
   python main.py
   ```

## Padrões de Código

### Python

- Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilize Type Hints sempre que possível
- Documente todas as funções e classes usando docstrings
- Mantenha os nomes de variáveis e funções em português para manter consistência com o projeto

### HTML/CSS/JavaScript

- Use 2 espaços para indentação em HTML, CSS e JavaScript
- Mantenha os nomes de classes CSS semanticamente claros
- Siga o padrão Bootstrap para componentes de interface
- Mantenha todo o texto em português

## Testes

- Escreva testes para suas implementações
- Execute os testes antes de submeter o Pull Request
- Certifique-se de que todos os testes estão passando

## Processo de Pull Request

1. Descreva claramente o que foi alterado
2. Inclua capturas de tela para mudanças visuais
3. Referencie as issues que este PR resolve (ex: "Resolve #123")
4. Certifique-se de que seu código está formatado de acordo com os padrões do projeto

## Reportando Bugs

Se você encontrar um bug, por favor, crie uma issue incluindo:

- Descrição clara e concisa do problema
- Passos para reproduzir
- Comportamento esperado vs. comportamento atual
- Capturas de tela (se aplicável)
- Informações do ambiente (sistema operacional, navegador, etc.)

## Solicitação de Features

Se você tem uma ideia para uma nova funcionalidade:

1. Crie uma issue com o título "Feature: [nome da feature]"
2. Descreva detalhadamente a funcionalidade proposta
3. Explique por que essa feature seria útil para o projeto

## Perguntas?

Se você tiver alguma dúvida sobre como contribuir, sinta-se à vontade para criar uma issue marcada como "Pergunta" ou entre em contato com a equipe de desenvolvimento.

Obrigado por contribuir com o VigiAPP!