import os
from pathlib import Path
from config import config

def setup_security():
    """Configura o sistema de segurança"""
    print("Configuração do Sistema de Segurança - VigiAPP")
    print("=" * 50)
    
    # Criar diretórios necessários
    Path('logs').mkdir(exist_ok=True)
    Path('backups').mkdir(exist_ok=True)
    
    # Verificar configurações de email
    print("\nVerificando configurações de email...")
    if config.validate_email_config():
        print("✓ Configurações de email estão completas")
        print(f"✓ Usando email: {config.SMTP_USER}")
    else:
        print("\nPara configurar o email, crie um arquivo .env com as seguintes variáveis:")
        print("""
GMAIL_USERNAME=vigiappcpv@gmail.com
GMAIL_PASSWORD=sua-senha-de-app
        """)
    
    # Verificar configurações de segurança
    print("\nConfigurações de segurança atuais:")
    security_config = config.get_security_config()
    for key, value in security_config.items():
        print(f"- {key}: {value}")
    
    print("\nPara personalizar os limites, adicione ao arquivo .env:")
    print("""
SECURITY_LOGIN_ATTEMPTS=5
SECURITY_FAILED_LOGINS=3
SECURITY_SUSPICIOUS_IPS=3
SECURITY_FILE_CHANGES=10
    """)
    
    # Verificar permissões
    print("\nVerificando permissões...")
    try:
        log_file = Path('logs/security.log')
        log_file.touch(exist_ok=True)
        os.chmod(log_file, 0o644)
        print("✓ Permissões dos logs configuradas")
    except Exception as e:
        print(f"✗ Erro ao configurar permissões: {str(e)}")
    
    print("\nConfiguração concluída!")
    print("\nPróximos passos:")
    print("1. Configure as variáveis de ambiente no arquivo .env")
    print("2. Reinicie o aplicativo para aplicar as configurações")
    print("3. Monitore os logs em logs/security.log")

if __name__ == '__main__':
    setup_security() 