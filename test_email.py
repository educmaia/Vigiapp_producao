from email_sender import EmailSender
from utils import get_brasil_datetime
import os

def test_mailersend():
    # Obtém a chave API do ambiente
    api_key = os.environ.get('MAILERSEND_API_KEY')
    if not api_key:
        print("❌ MAILERSEND_API_KEY não encontrada no ambiente.")
        return
    
    # Cria instância do EmailSender
    sender = EmailSender(api_key)
    
    # Verifica se o email está habilitado
    if not sender.email_enabled:
        print("❌ Sistema de email está desabilitado.")
        return
    
    # Prepara o conteúdo do email de teste
    subject = "VigiAPP - Teste de Integração MailerSend"
    
    # Obtém a data/hora atual
    now = get_brasil_datetime()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Conteúdo HTML
    html_content = f"""
    <html>
    <body>
        <h2>VigiAPP - Teste de Integração MailerSend</h2>
        <p>Este é um email de teste enviado pelo sistema VigiAPP utilizando a API do MailerSend.</p>
        <p>Data e hora do envio: {timestamp}</p>
        <p>Se você está visualizando este email, a integração foi concluída com sucesso!</p>
        <hr>
        <p style="font-size: 12px; color: #666;">
            Este é um email automático, favor não responder.
        </p>
    </body>
    </html>
    """
    
    # Define destinatário (para testes, usamos o padrão)
    to_emails = None  # Usará o destinatário padrão (clt.cpv@ifsp.edu.br)
    
    # Tenta enviar o email
    print("🔄 Enviando email de teste...")
    success, response = sender.send_email(subject, html_content, to_emails)
    
    # Verifica o resultado
    if success:
        print("✅ Email de teste enviado com sucesso!")
        print(f"✅ Resposta: {response}")
    else:
        print(f"❌ Falha ao enviar email: {response}")

if __name__ == "__main__":
    test_mailersend()