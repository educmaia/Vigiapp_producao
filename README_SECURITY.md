# Sistema de Alertas de Segurança - VigiAPP

Este sistema monitora e alerta sobre atividades suspeitas no VigiAPP.

## Funcionalidades

- Monitoramento de tentativas de login
- Monitoramento de IPs suspeitos
- Monitoramento de alterações em arquivos
- Alertas por email
- Logs detalhados de segurança
- Histórico de alertas

## Configuração

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure as variáveis de ambiente no arquivo `.env`:
   - `SMTP_SERVER`: Servidor SMTP para envio de emails
   - `SMTP_PORT`: Porta do servidor SMTP
   - `SMTP_USER`: Usuário do email
   - `SMTP_PASSWORD`: Senha do email
   - `ALERT_EMAIL`: Email para receber os alertas

3. Para Gmail, você precisará:
   - Ativar a verificação em duas etapas
   - Gerar uma senha de app específica para o VigiAPP

## Limites de Alertas

O sistema monitora e alerta sobre:

1. Tentativas de Login:
   - Alerta após 5 tentativas em 1 hora
   - Registra IP e horário das tentativas

2. IPs Suspeitos:
   - Alerta após 3 ocorrências suspeitas em 24 horas
   - Monitora padrões de acesso anormais

3. Alterações em Arquivos:
   - Alerta após 10 alterações em 24 horas
   - Monitora arquivos sensíveis do sistema

## Logs

Os logs são armazenados em:
- `logs/security.log`: Log detalhado das atividades de segurança
- `logs/security_alerts.json`: Histórico de alertas em formato JSON

## Monitoramento

Para monitorar o sistema:

1. Verifique os logs de segurança:
   ```bash
   tail -f logs/security.log
   ```

2. Verifique o histórico de alertas:
   ```bash
   cat logs/security_alerts.json
   ```

3. Verifique os emails de alerta na caixa de entrada configurada

## Personalização

Você pode ajustar os limites de alerta modificando as variáveis de ambiente:
- `SECURITY_LOGIN_ATTEMPTS`
- `SECURITY_FAILED_LOGINS`
- `SECURITY_SUSPICIOUS_IPS`
- `SECURITY_FILE_CHANGES`

## Solução de Problemas

Se os alertas não estiverem funcionando:

1. Verifique as configurações de email no arquivo `.env`
2. Verifique os logs em `logs/security.log`
3. Teste o envio de email manualmente
4. Verifique se as permissões dos arquivos de log estão corretas

## Recomendações

1. Configure um email dedicado para receber os alertas
2. Revise regularmente os logs de segurança
3. Mantenha as configurações de email atualizadas
4. Considere implementar bloqueio de IP após múltiplos alertas 