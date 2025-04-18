from email_smtp import EmailSender
from utils import get_brasil_datetime
import os
import json

def test_mailersend_direct():
    """Teste direto da biblioteca MailerSend sem usar nossa classe personalizada"""
    api_key = os.environ.get('MAILERSEND_API_KEY')
    if not api_key:
        print("❌ MAILERSEND_API_KEY não encontrada no ambiente.")
        return

    print(f"Usando API key (primeiros 4 caracteres): {api_key[:4]}...")
    
    try:
        # Cria uma nova instância de email diretamente com a biblioteca
        mail = NewEmail(api_key)
        
        # Cria o objeto de mensagem
        message = {}
        
        # Configura o remetente usando um email do domínio mailersend.net (que não precisa de verificação)
        mail.set_mail_from({"email": "noreply@mailersend.net", "name": "VigiAPP Test"}, message)
        
        # Configura os destinatários
        recipients = [{"email": "clt.cpv@ifsp.edu.br", "name": "Coordenadoria de Licitações e Contratos"}]
        mail.set_mail_to(recipients, message)
        
        # Configura o assunto
        mail.set_subject("VigiAPP - Teste Direto MailerSend", message)
        
        # Configura o conteúdo HTML
        now = get_brasil_datetime()
        timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
        
        html_content = f"""
        <html>
        <body>
            <h2>VigiAPP - Teste Direto MailerSend</h2>
            <p>Este é um email de teste enviado usando diretamente a biblioteca MailerSend.</p>
            <p>Data e hora do envio: {timestamp}</p>
            <p>Se você está visualizando este email, a integração está correta!</p>
        </body>
        </html>
        """
        mail.set_html_content(html_content, message)
        
        # Tenta enviar o email
        print("🔄 Enviando email direto via MailerSend...")
        print(f"🔄 Conteúdo da mensagem: {json.dumps(message, indent=2)}")
        
        response = mail.send(message)
        
        print(f"🔄 Tipo de resposta: {type(response)}")
        print(f"🔄 Resposta completa: {response}")
        
        if response and hasattr(response, 'status_code'):
            if response.status_code < 400:
                print(f"✅ Email enviado com sucesso! Status code: {response.status_code}")
                return True
            else:
                print(f"❌ Falha ao enviar email. Status code: {response.status_code}")
                print(f"❌ Resposta detalhada: {response.text if hasattr(response, 'text') else 'Sem detalhes'}")
                return False
        else:
            print(f"❌ Resposta inválida ou nula do servidor MailerSend")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste direto: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mailersend():
    # Obtém a chave API do ambiente
    api_key = os.environ.get('MAILERSEND_API_KEY')
    if not api_key:
        print("❌ MAILERSEND_API_KEY não encontrada no ambiente.")
        return
    
    print("\n==== TESTE USANDO NOSSA CLASSE EMAIL SENDER ====\n")
    
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
    print("\n==== TESTE DIRETO COM A BIBLIOTECA MAILERSEND ====\n")
    test_mailersend_direct()
    test_mailersend()