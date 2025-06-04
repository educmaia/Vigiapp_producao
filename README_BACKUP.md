# Sistema de Backup Automático - VigiAPP

Este sistema realiza backups automáticos regulares do banco de dados e arquivos do VigiAPP.

## Funcionalidades

- Backup automático do banco de dados SQLite
- Backup automático da pasta de uploads
- Compressão dos arquivos de backup
- Limpeza automática de backups antigos (mais de 30 dias)
- Logs detalhados das operações
- Agendamento via cron job

## Estrutura de Diretórios

```
vigiapp/
├── backups/           # Diretório onde os backups são armazenados
├── logs/             # Logs do sistema de backup
│   ├── backup.log    # Log principal do backup
│   └── cron.log      # Log do cron job
├── backup.py         # Script principal de backup
└── setup_backup_cron.py  # Script para configurar o cron job
```

## Configuração

1. Certifique-se de que o Python 3 está instalado no sistema
2. Execute o script de configuração do cron job:
   ```bash
   python3 setup_backup_cron.py
   ```

## Agendamento

O backup é executado automaticamente todos os dias às 2:00 da manhã.

## Formato dos Backups

- Banco de dados: `db_backup_YYYYMMDD_HHMMSS.db.gz`
- Uploads: `uploads_backup_YYYYMMDD_HHMMSS.zip`

## Logs

Os logs são armazenados em:
- `logs/backup.log`: Log detalhado das operações de backup
- `logs/cron.log`: Log da execução via cron

## Manutenção

- Os backups são mantidos por 30 dias
- Backups antigos são removidos automaticamente
- Os logs são rotacionados quando atingem 1MB

## Restauração

Para restaurar um backup:

1. Banco de dados:
   ```bash
   gunzip db_backup_YYYYMMDD_HHMMSS.db.gz
   cp db_backup_YYYYMMDD_HHMMSS.db controle_portaria.db
   ```

2. Uploads:
   ```bash
   unzip uploads_backup_YYYYMMDD_HHMMSS.zip
   ```

## Monitoramento

Verifique regularmente:
- O diretório `backups/` para confirmar que novos backups estão sendo criados
- O arquivo `logs/backup.log` para verificar se há erros
- O arquivo `logs/cron.log` para verificar a execução do cron job

## Solução de Problemas

Se o backup não estiver funcionando:

1. Verifique se o cron está ativo:
   ```bash
   crontab -l
   ```

2. Verifique os logs:
   ```bash
   tail -f logs/backup.log
   tail -f logs/cron.log
   ```

3. Execute o backup manualmente para testar:
   ```bash
   python3 backup.py
   ``` 