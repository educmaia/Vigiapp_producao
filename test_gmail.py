import os
from email_smtp import EmailSender
from flask import Flask
from utils import get_brasil_datetime

def test_gmail_smtp():
    """
    Testa o envio de email usando o SMTP do Gmail.
    Requer as variáveis de ambiente GMAIL_PASSWORD configuradas.
    """
    # Cria um aplicativo Flask para o teste
    app = Flask(__name__)
    
    # Configura o contexto do aplicativo
    with app.app_context():
        # Obtém a senha do Gmail do ambiente
        gmail_password = os.environ.get('GMAIL_PASSWORD')
        if not gmail_password:
            print("❌ GMAIL_PASSWORD não encontrada no ambiente.")
            return False
        
        print("\n==== TESTE DE ENVIO DE EMAIL VIA GMAIL SMTP ====\n")
        
        # Cria uma instância do EmailSender
        sender = EmailSender(app=app)
        
        # Verifica se o email está habilitado
        if not sender.email_enabled:
            print("❌ Sistema de email está desabilitado.")
            return False
        
        # Prepara o conteúdo do email de teste
        subject = "VigiAPP - Teste de Email via Gmail SMTP"
        
        # Obtém a data/hora atual
        now = get_brasil_datetime()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Conteúdo HTML
        html_content = f"""
        <html>
        <body>
            <h2>VigiAPP - Teste de Integração com Gmail</h2>
            <p>Este é um email de teste enviado pelo sistema VigiAPP utilizando SMTP do Gmail.</p>
            <p>Data e hora do envio: {timestamp}</p>
            <p>Se você está visualizando este email, a integração foi concluída com sucesso!</p>
            <hr>
            <p style="font-size: 12px; color: #666;">
                Este é um email automático, favor não responder.
            </p>
        </body>
        </html>
        """
        
        # Define destinatário (para testes)
        to_emails = [
            {"email": "clt.cpv@ifsp.edu.br", "name": "Coordenadoria de Licitações e Contratos"}
        ]
        
        # Tenta enviar o email
        print("🔄 Enviando email de teste via Gmail SMTP...")
        success, response = sender.send_email(subject, html_content, to_emails)
        
        # Verifica o resultado
        if success:
            print("✅ Email de teste enviado com sucesso via Gmail!")
            print(f"✅ Resposta: {response}")
            return True
        else:
            print(f"❌ Falha ao enviar email: {response}")
            return False

if __name__ == "__main__":
    test_gmail_smtp()