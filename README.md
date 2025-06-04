# VigiAPP - Sistema de Controle de Acesso

Sistema de controle de acesso desenvolvido para gerenciar entrada e saída de pessoas, veículos e correspondências em condomínios e empresas.

## Funcionalidades

- Controle de acesso de pessoas
- Gerenciamento de ingressos
- Cadastro de empresas
- Controle de entregas
- Gestão de correspondências
- Registro de ocorrências
- Geração de relatórios
- Sistema de QR Code para acesso rápido

## Requisitos

- Python 3.8+
- PostgreSQL
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/vigiapp.git
cd vigiapp
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
python run.py
```

## Uso

Para iniciar o servidor:
```bash
python run.py
```

Acesse o sistema em: http://localhost:5000

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.