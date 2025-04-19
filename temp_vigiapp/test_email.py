from email_smtp import EmailSender
from utils import get_brasil_datetime
import os
import json
from flask import Flask

def test_gmail_smtp():
    """Teste de envio de email usando Flask-Mail com Gmail SMTP"""
    print("\n==== TESTE DE ENVIO DE EMAIL COM FLASK-MAIL E GMAIL SMTP ====\n")
    
    # Verificando se a senha do Gmail está configurada
    gmail_password = os.environ.get('GMAIL_PASSWORD')
    if not gmail_password:
        print("❌ GMAIL_PASSWORD não encontrada no ambiente. Impossível enviar emails.")
        return False
    
    # Criando uma aplicação Flask temporária para teste
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'vigiappcpv@gmail.com'
    app.config['MAIL_PASSWORD'] = gmail_password
    app.config['MAIL_DEFAULT_SENDER'] = ('VigiAPP - Sistema de Controle de Acesso', 'vigiappcpv@gmail.com')
    
    # Inicializando o EmailSender
    with app.app_context():
        sender = EmailSender(app)
        
        # Preparando o email de teste
        subject = "VigiAPP - Teste de Email via Gmail SMTP"
        
        # Obtendo a data/hora atual no formato brasileiro
        now = get_brasil_datetime()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # Conteúdo HTML do email de teste
        html_content = f"""
        <html>
        <body>
            <table style="width: auto; border-collapse: collapse;">
                <tr>
                    <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                        <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                    </a></td>
                    <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                </tr>
            </table>
            
            <h2>Teste de Envio de Email</h2>
            
            <p>Este é um email de teste enviado pelo sistema VigiAPP utilizando Gmail SMTP através do Flask-Mail.</p>
            <p>Data e hora do envio: {timestamp}</p>
            <p>Se você está visualizando este email, a integração foi concluída com sucesso!</p>
            
            <hr>
            <p style="font-size: 12px; color: #666;">
                Este é um email automático, favor não responder.
            </p>
        </body>
        </html>
        """
        
        # Destinatário padrão
        to_emails = ["clt.cpv@ifsp.edu.br"]
        
        # Tentando enviar o email
        print("🔄 Enviando email de teste via Gmail SMTP...")
        success, response = sender.send_email(subject, html_content, to_emails)
        
        # Verificando o resultado
        if success:
            print("✅ Email de teste enviado com sucesso!")
            print(f"✅ Detalhes: {response}")
            return True
        else:
            print(f"❌ Falha ao enviar email: {response}")
            return False

if __name__ == "__main__":
    test_gmail_smtp()