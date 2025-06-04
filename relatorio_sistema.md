# Relatório Técnico e Operacional - VigiApp
## Sistema de Controle de Portaria

### Sumário
1. [Introdução](#1-introdução)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Componentes Principais](#3-componentes-principais)
4. [Funcionalidades Detalhadas](#4-funcionalidades-detalhadas)
5. [Fluxos de Operação](#5-fluxos-de-operação)
6. [Segurança e Autenticação](#6-segurança-e-autenticação)
7. [Integrações](#7-integrações)
8. [Manutenção e Suporte](#8-manutenção-e-suporte)
9. [Recomendações](#9-recomendações)
10. [Conclusão](#10-conclusão)

### 1. Introdução

O VigiApp é um sistema web desenvolvido em Python utilizando o framework Flask, projetado para gerenciar e automatizar processos de portaria em ambientes corporativos. Este relatório apresenta uma análise detalhada da arquitetura, funcionalidades e operação do sistema.

#### 1.1 Objetivos do Sistema
- Automatizar o controle de acesso de visitantes
- Gerenciar entregas e correspondências
- Registrar e monitorar ocorrências
- Gerar relatórios e estatísticas
- Facilitar o processo de check-in/check-out
- Melhorar a segurança e o controle de acesso

#### 1.2 Público-Alvo
- Porteiros e recepcionistas
- Equipe de segurança
- Administradores do sistema
- Gestores de instalações

### 2. Arquitetura do Sistema

#### 2.1 Tecnologias Utilizadas
- **Backend**: Python 3.x com Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Banco de Dados**: SQLAlchemy com SQLite
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **Email**: Flask-Mail
- **QR Code**: qrcode

#### 2.2 Estrutura do Projeto
```
vigiapp/
├── app.py                 # Configuração principal do Flask
├── models.py             # Modelos de dados
├── forms.py              # Formulários
├── utils.py              # Funções utilitárias
├── qr_code.py            # Geração de QR codes
├── email_smtp.py         # Configuração de email
├── routes/               # Rotas da aplicação
├── templates/            # Templates HTML
├── static/              # Arquivos estáticos
└── instance/            # Arquivos de instância
```

#### 2.3 Padrões de Design
- MVC (Model-View-Controller)
- Blueprint para organização de rotas
- Factory Pattern para criação da aplicação
- Repository Pattern para acesso a dados

### 3. Componentes Principais

#### 3.1 Modelos de Dados
1. **User**
   - Gerenciamento de usuários
   - Níveis de acesso (admin, operador)
   - Autenticação e autorização

2. **Pessoa**
   - Cadastro de visitantes
   - Informações pessoais
   - Histórico de visitas

3. **Ingresso**
   - Registro de entradas/saídas
   - Motivo da visita
   - QR Code de acesso

4. **Entrega**
   - Controle de entregas
   - Status de entrega
   - Destinatário

5. **Correspondência**
   - Gestão de correspondências
   - Tipo de correspondência
   - Status de entrega

6. **Ocorrência**
   - Registro de incidentes
   - Nível de gravidade
   - Ações tomadas

#### 3.2 Formulários
1. **IngressoForm**
   - Validação de CPF
   - Campos obrigatórios
   - Formatação de data/hora

2. **PessoaForm**
   - Validação de dados pessoais
   - Máscaras de entrada
   - Campos customizados

3. **OcorrênciaForm**
   - Classificação de gravidade
   - Descrição detalhada
   - Anexos

### 4. Funcionalidades Detalhadas

#### 4.1 Gestão de Visitantes
1. **Cadastro**
   - Validação de CPF
   - Foto do visitante
   - Histórico de visitas
   - Empresa/Instituição

2. **Registro de Entrada**
   - Geração automática de QR Code
   - Notificação por email
   - Registro de horário
   - Motivo da visita

3. **Registro de Saída**
   - Check-out rápido
   - Tempo de permanência
   - Relatório de visita

#### 4.2 Sistema de QR Code
1. **Geração**
   - Código único por ingresso
   - Validação de tempo
   - Informações do visitante

2. **Leitura**
   - Scanner de QR Code
   - Validação de acesso
   - Registro automático

#### 4.3 Gestão de Entregas
1. **Registro**
   - Tipo de entrega
   - Destinatário
   - Status
   - Notificações

2. **Controle**
   - Rastreamento
   - Confirmação de recebimento
   - Histórico

#### 4.4 Correspondências
1. **Cadastro**
   - Tipo de correspondência
   - Prioridade
   - Destinatário

2. **Distribuição**
   - Rastreamento
   - Confirmação
   - Notificações

#### 4.5 Ocorrências
1. **Registro**
   - Classificação
   - Descrição
   - Gravidade
   - Ações

2. **Acompanhamento**
   - Status
   - Responsáveis
   - Resolução

### 5. Fluxos de Operação

#### 5.1 Check-in de Visitante
1. Identificação do visitante
2. Validação de dados
3. Geração de ingresso
4. Emissão de QR Code
5. Notificação por email

#### 5.2 Check-out de Visitante
1. Leitura do QR Code
2. Registro de saída
3. Cálculo de permanência
4. Atualização de status

#### 5.3 Gestão de Entregas
1. Registro da entrega
2. Notificação do destinatário
3. Confirmação de recebimento
4. Atualização de status

### 6. Segurança e Autenticação

#### 6.1 Sistema de Login
- Autenticação segura
- Níveis de acesso
- Sessões controladas
- Proteção CSRF

#### 6.2 Controle de Acesso
- Permissões por função
- Registro de atividades
- Logs de sistema
- Backup automático

### 7. Integrações

#### 7.1 Sistema de Email
- Notificações automáticas
- Templates personalizados
- Confirmações
- Alertas

#### 7.2 Relatórios
- Exportação em PDF
- Filtros personalizados
- Gráficos e estatísticas
- Históricos

### 8. Manutenção e Suporte

#### 8.1 Backup
- Backup automático
- Recuperação de dados
- Versionamento
- Logs de sistema

#### 8.2 Monitoramento
- Logs de acesso
- Erros do sistema
- Performance
- Uso de recursos

### 9. Recomendações

#### 9.1 Melhorias Sugeridas
1. Implementação de API REST
2. Sistema de notificações push
3. App mobile para visitantes
4. Integração com câmeras
5. Sistema de agendamento

#### 9.2 Boas Práticas
1. Manutenção regular
2. Atualizações de segurança
3. Backup periódico
4. Monitoramento contínuo
5. Treinamento de usuários

### 10. Conclusão

O VigiApp representa uma solução robusta e completa para o gerenciamento de portaria, oferecendo funcionalidades essenciais para o controle de acesso, gestão de visitantes e segurança. Sua arquitetura modular e escalável permite adaptações e melhorias contínuas, mantendo o sistema atualizado com as necessidades do ambiente corporativo.

#### 10.1 Pontos Fortes
- Interface intuitiva
- Processos automatizados
- Segurança robusta
- Relatórios detalhados
- Fácil manutenção

#### 10.2 Próximos Passos
1. Implementação de novas funcionalidades
2. Expansão do sistema
3. Melhorias de performance
4. Integrações adicionais
5. Treinamento de usuários 