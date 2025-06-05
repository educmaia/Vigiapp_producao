import os
import threading
from flask import current_app
from flask_mail import Mail, Message
from utils import get_brasil_datetime

class EmailSender:
    def __init__(self, app=None, username=None, password=None):
        self.email_enabled = False
        self.dev_mode = False  # Modo de produção por padrão
        self.mail = None
        self.sender_email = "vigiappcpv@gmail.com"
        self.sender_name = "VigiAPP - Sistema de Controle de Acesso"
        
        try:
            # Obtém as credenciais do ambiente ou dos parâmetros
            self.username = username or os.environ.get('GMAIL_USERNAME', self.sender_email)
            self.password = password or os.environ.get('GMAIL_PASSWORD')
            
            # Se não houver senha, o sistema de email fica desabilitado
            if not self.password:
                print("AVISO: GMAIL_PASSWORD não encontrada. Sistema de email desabilitado.")
                if current_app:
                    current_app.logger.warning("GMAIL_PASSWORD não encontrada. Sistema de email desabilitado.")
                return
            
            # Se foi passado um app Flask, configura o Flask-Mail
            if app:
                self.init_app(app)
            
            # Marca como habilitado
            self.email_enabled = True
            print(f"Sistema de email inicializado com sucesso para: {self.username}")
            
            # Em ambiente de desenvolvimento, mostra aviso sobre simulação de envio
            if self.dev_mode:
                print("⚠️ Modo de desenvolvimento ativado - os emails serão simulados mas não enviados realmente")
                
        except Exception as e:
            print(f"Erro ao inicializar sistema de email: {e}")
            if current_app:
                current_app.logger.error(f"Erro ao inicializar sistema de email: {e}")
    
    def init_app(self, app):
        """Inicializa o Flask-Mail com um aplicativo Flask"""
        # Configura o Flask-Mail
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = self.username
        app.config['MAIL_PASSWORD'] = self.password
        app.config['MAIL_DEFAULT_SENDER'] = (self.sender_name, self.sender_email)
        
        # Inicializa o Flask-Mail
        self.mail = Mail(app)
        print("Flask-Mail inicializado e configurado")

    def _send_email_thread(self, subject, html_content, recipients, attachments, app):
        with app.app_context():
            try:
                # Cria a mensagem
                msg = Message(
                    subject=subject,
                    recipients=recipients,
                    html=html_content,
                    sender=(self.sender_name, self.sender_email)
                )

                # Adiciona anexos se houver
                if attachments:
                    for attachment_info in attachments:
                        try:
                            with open(attachment_info['filepath'], 'rb') as f:
                                msg.attach(
                                    filename=attachment_info['filename'],
                                    content_type=attachment_info.get('type', 'application/octet-stream'),
                                    data=f.read()
                                )
                        except Exception as e:
                            current_app.logger.error(f"Erro ao anexar arquivo {attachment_info['filepath']}: {e}")
                            print(f"❌ Erro ao anexar arquivo: {e}")

                # Envia o email
                if self.mail:
                    self.mail.send(msg)
                    current_app.logger.info(f"Email enviado via Flask-Mail para {', '.join([r[1] if isinstance(r, tuple) else r for r in recipients])}")
                    print("✅ Email enviado com sucesso via Flask-Mail")
                else:
                    error_message = "Flask-Mail não inicializado. Use init_app() ou forneça o app no construtor."
                    current_app.logger.error(error_message)
                    print(f"❌ {error_message}")

            except Exception as e:
                error_message = f"Erro ao enviar email na thread: {str(e)}"
                current_app.logger.error(error_message)
                print(f"❌ {error_message}")

    def send_email(self, subject, html_content, to_emails=None, attachments=None):
        """
        Envia um email com anexos opcionais para múltiplos destinatários usando SMTP do Gmail.
        Em modo de desenvolvimento, simula o envio de email mas não realiza o envio real.
        O envio real é feito em uma thread separada.
        
        Args:
            subject (str): Assunto do email
            html_content (str): Conteúdo HTML do email
            to_emails (list): Lista de emails ou dicionários com emails dos destinatários 
                             (se None, usa clt.cpv@ifsp.edu.br)
            attachments (list): Lista de dicionários com informações dos anexos:
                                [{'filepath': '/caminho/arquivo.jpg', 'filename': 'arquivo.jpg', 'type': 'image/jpeg'}]
        
        Returns:
            tuple: (bool, response) indicando sucesso/falha e resposta/erro
        """
        if not self.email_enabled:
            if current_app:
                current_app.logger.warning("Sistema de email está desabilitado. Tentativa de envio de email ignorada.")
            return False, "Sistema de email desabilitado"

        if to_emails is None:
            to_emails = [{"email": "clt.cpv@ifsp.edu.br", "name": "Coordenadoria de Licitações e Contratos"}]

        recipients = []
        for recipient in to_emails:
            if isinstance(recipient, dict):
                email = recipient.get("email")
                name = recipient.get("name", "")
                recipients.append((name, email) if name else email)
            else:
                recipients.append(recipient)

        if self.dev_mode:
            # Simulação de envio em modo de desenvolvimento
            print("📧 MODO DE SIMULAÇÃO DE EMAIL ATIVADO (Chamada send_email)")
            print(f"📧 Assunto: {subject}")
            print(f"📧 Para: {', '.join([r[1] if isinstance(r, tuple) else r for r in recipients])}")
            if attachments:
                print(f"📧 Anexos: {', '.join([a['filename'] for a in attachments])}")
            print("📧 EMAIL SIMULADO COM SUCESSO (Chamada send_email)")
            if current_app:
                emails_str = ', '.join([r[1] if isinstance(r, tuple) else r for r in recipients])
                current_app.logger.info(f"Email simulado para {emails_str}: {subject}")
            return True, {"simulated": True, "message": "Email simulado com sucesso"}

        # Envio real em uma nova thread
        try:
            app = current_app._get_current_object()
            thread = threading.Thread(
                target=self._send_email_thread,
                args=(subject, html_content, recipients, attachments, app)
            )
            thread.start()
            
            print(f"✅ Thread de envio de email iniciada para: {', '.join([r[1] if isinstance(r, tuple) else r for r in recipients])}")
            if current_app:
                 current_app.logger.info(f"Thread de envio de email iniciada para {', '.join([r[1] if isinstance(r, tuple) else r for r in recipients])}: {subject}")
            return True, "Email sending initiated"

        except Exception as e:
            error_message = f"Erro ao iniciar thread de envio de email: {str(e)}"
            print(f"❌ {error_message}")
            if current_app:
                current_app.logger.error(error_message)
            return False, error_message
    
    def enviar_email_pessoa(self, cpf, nome, telefone, empresa, motivo, pessoa_setor, observacoes):
        subject = "VigiAPP - Nova Visita Inserida"
        
        # Conteúdo HTML da mensagem com horário brasileiro
        dia_e_hora_atual = get_brasil_datetime()
        diaehoradeenvio = dia_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        html_content = f"""
                    <table style="width: auto; border-collapse: collapse;">
                        <!-- TABELA DE REGISTRO -->
                        <tbody><tr>
                            <!-- IMAGEM -->
                            <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                                <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                            </a></td>
                            <!-- Título VIGIAPP -->
                            <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                        </tr>
                        <!-- Segunda linha da tabela -->
                        <tr>
                            <!-- NOVO REGISTRO -->
                            <td style="border: 0;"><strong>NOVA VISITA:</strong></td>
                            <!-- INFORMAÇÃO -->
                            <td style="border: 0;">CPF: {cpf}<br>Nome: {nome}<br>Telefone: {telefone}<br>Empresa: {empresa}<br>Motivo: {motivo}<br>Pessoa/Setor: {pessoa_setor}<br>Observações: {observacoes}<br>Dia e Hora de Registro:{diaehoradeenvio}</td>
                        </tr>
                    </tbody></table>
                    """
        
        return self.send_email(subject, html_content)
        
    def enviar_email_ingresso(self, ingresso, pessoa):
        """Envia email notificando o registro de um novo ingresso"""
        subject = "VigiAPP - Novo Ingresso Registrado"
        
        # Conteúdo HTML da mensagem com horário brasileiro
        dia_e_hora_atual = get_brasil_datetime()
        diaehoradeenvio = dia_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        
        # Formatação do texto da observação para substituir quebras de linha por tags HTML
        observacoes_formatadas = ingresso.observacoes.replace('\n', '<br>') if ingresso.observacoes else "-"
        
        # Status de saída formatado com estilo
        if ingresso.saida:
            status_saida = f'<span style="color: green;">{ingresso.saida}</span>'
        else:
            status_saida = '<span style="color: orange; font-style: italic;">Não registrada</span>'
        
        html_content = f"""
                    <html>
                    <body>
                        <table style="width: auto; border-collapse: collapse;">
                            <!-- TABELA DE REGISTRO -->
                            <tbody><tr>
                                <!-- IMAGEM -->
                                <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                                    <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                                </a></td>
                                <!-- Título VIGIAPP -->
                                <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                            </tr>
                        </tbody></table>
                        
                        <h2>Novo Ingresso Registrado</h2>
                        
                        <h3>Informações da Pessoa:</h3>
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                            <p><strong>CPF:</strong> {pessoa.cpf}</p>
                            <p><strong>Nome:</strong> {pessoa.nome}</p>
                            <p><strong>Telefone:</strong> {pessoa.telefone or "-"}</p>
                            <p><strong>Empresa:</strong> {pessoa.empresa or "-"}</p>
                        </div>
                        
                        <h3>Informações do Ingresso:</h3>
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
                            <p><strong>Data:</strong> {ingresso.data}</p>
                            <p><strong>Entrada:</strong> <span style="color: blue;">{ingresso.entrada}</span></p>
                            <p><strong>Saída:</strong> {status_saida}</p>
                            <p><strong>Motivo:</strong> {ingresso.motivo}</p>
                            <p><strong>Pessoa/Setor:</strong> {ingresso.pessoa_setor}</p>
                            
                            <div style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 10px;">
                                <p><strong>Observações:</strong></p>
                                <div style="background-color: white; padding: 8px; border-left: 4px solid #2f9e41;">
                                    {observacoes_formatadas}
                                </div>
                            </div>
                        </div>
                        
                        <p><em>Email enviado em: {diaehoradeenvio}</em></p>
                        
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                            Este é um email automático enviado pelo sistema VigiAPP. Favor não responder.
                        </p>
                    </body>
                    </html>
                    """
        
        return self.send_email(subject, html_content)
    
    def enviar_email_correspondencia(self, remetente, destinatario, tipo, setor, data_recebimento, hora_recebimento):
        subject = "VigiAPP - Nova Correspondência Registrada"
        
        # Conteúdo HTML da mensagem com horário brasileiro
        dia_e_hora_atual = get_brasil_datetime()
        diaehoradeenvio = dia_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        
        # Cores para os diferentes tipos de correspondência
        cores_tipo = {
            'carta': '#3498db',  # azul
            'pacote': '#f39c12',  # laranja
            'encomenda': '#e74c3c',  # vermelho
            'documento': '#2ecc71',  # verde
            'outros': '#95a5a6'   # cinza
        }
        
        cor_tipo = cores_tipo.get(tipo.lower(), '#95a5a6')
        
        html_content = f"""
                    <html>
                    <body>
                        <table style="width: auto; border-collapse: collapse;">
                            <!-- TABELA DE REGISTRO -->
                            <tbody><tr>
                                <!-- IMAGEM -->
                                <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                                    <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                                </a></td>
                                <!-- Título VIGIAPP -->
                                <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                            </tr>
                        </tbody></table>
                        
                        <h2>Nova Correspondência Registrada</h2>
                        
                        <h3>Informações da Correspondência:</h3>
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                            <p><strong>Tipo:</strong> <span style="color: {cor_tipo}; font-weight: bold;">{tipo.upper()}</span></p>
                            <p><strong>Remetente:</strong> {remetente}</p>
                            <p><strong>Destinatário:</strong> {destinatario}</p>
                            <p><strong>Setor/Encomenda:</strong> {setor}</p>
                        </div>
                        
                        <h3>Informações de Recebimento:</h3>
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
                            <p><strong>Data de Recebimento:</strong> {data_recebimento}</p>
                            <p><strong>Hora de Recebimento:</strong> {hora_recebimento}</p>
                            <p><strong>Data de Registro:</strong> {diaehoradeenvio.split()[0]}</p>
                            <p><strong>Hora de Registro:</strong> {diaehoradeenvio.split()[1]}</p>
                        </div>
                        
                        <p><em>Email enviado em: {diaehoradeenvio}</em></p>
                        
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                            Este é um email automático enviado pelo sistema VigiAPP. Favor não responder.
                        </p>
                    </body>
                    </html>
                    """
        
        return self.send_email(subject, html_content)
    
    def enviar_email_ocorrencia(self, vigilante, envolvidos, data_registro, hora_registro, gravidade, ocorrencia):
        subject = "VigiAPP - Nova Ocorrência Registrada"
        
        # Conteúdo HTML da mensagem com horário brasileiro
        dia_e_hora_atual = get_brasil_datetime()
        diaehoradeenvio = dia_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        
        # Ajuste da formatação da gravidade para destacar visualmente
        estilo_gravidade = {
            'baixa': 'color: green;',
            'media': 'color: orange;',
            'alta': 'color: red; font-weight: bold;',
            'critica': 'color: red; font-weight: bold; text-transform: uppercase;'
        }
        
        estilo = estilo_gravidade.get(gravidade.lower(), '')
        
        # Formatação do texto da ocorrência para substituir quebras de linha por tags HTML
        ocorrencia_formatada = ocorrencia.replace('\n', '<br>')
        
        html_content = f"""
                    <html>
                    <body>
                        <table style="width: auto; border-collapse: collapse;">
                            <!-- TABELA DE REGISTRO -->
                            <tbody><tr>
                                <!-- IMAGEM -->
                                <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                                    <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                                </a></td>
                                <!-- Título VIGIAPP -->
                                <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                            </tr>
                        </tbody></table>
                        
                        <h2>Nova Ocorrência Registrada</h2>
                        
                        <h3>Informações da Ocorrência:</h3>
                        <p><strong>Vigilante Responsável:</strong> {vigilante}</p>
                        <p><strong>Envolvidos:</strong> {envolvidos}</p>
                        <p><strong>Data de Registro:</strong> {data_registro}</p>
                        <p><strong>Hora de Registro:</strong> {hora_registro}</p>
                        <p><strong>Gravidade:</strong> <span style="{estilo}">{gravidade.upper()}</span></p>
                        
                        <h3>Detalhes da Ocorrência:</h3>
                        <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #2f9e41; margin: 10px 0;">
                            {ocorrencia_formatada}
                        </div>
                        
                        <p><em>Email enviado em: {diaehoradeenvio}</em></p>
                        
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                            Este é um email automático enviado pelo sistema VigiAPP. Favor não responder.
                        </p>
                    </body>
                    </html>
                    """
        
        return self.send_email(subject, html_content)
    
    def enviar_email_entrega(self, entrega, empresa, imagens_paths=None):
        """
        Envia email notificando o registro de uma nova entrega com imagens anexadas
        
        Args:
            entrega: Objeto Entrega do modelo
            empresa: Objeto Empresa do modelo
            imagens_paths: Lista de dicionários com caminhos e nomes das imagens
                           [{
                                'filepath': '/path/to/img.jpg',
                                'filename': 'img.jpg',
                                'type': 'image/jpeg'
                           }]
        """
        subject = "VigiAPP - Nova Entrega Registrada"
        
        # Conteúdo HTML da mensagem com horário brasileiro
        dia_e_hora_atual = get_brasil_datetime()
        diaehoradeenvio = dia_e_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        
        # Verifica se há imagens para anexar
        imagens_count = len(entrega.imagens) if hasattr(entrega, 'imagens') and entrega.imagens else 0
        
        html_content = f"""
                    <html>
                    <body>
                        <table style="width: auto; border-collapse: collapse;">
                            <!-- TABELA DE REGISTRO -->
                            <tbody><tr>
                                <!-- IMAGEM -->
                                <td style="border: 0;"><a href="https://ibb.co/mJsWTzD">
                                    <img src="https://i.ibb.co/SNTCyvs/vigiapp.jpg" alt="vigiapp" border="0" width="125">
                                </a></td>
                                <!-- Título VIGIAPP -->
                                <td style="text-align: center; font-size: 20px;"><strong>VIGIAPP em AÇÃO</strong></td>
                            </tr>
                        </tbody></table>
                        
                        <h2>Nova Entrega Registrada</h2>
                        <h3>Informações da Empresa:</h3>
                        <p><strong>CNPJ:</strong> {empresa.cnpj}</p>
                        <p><strong>Nome da Empresa:</strong> {empresa.nome_empresa}</p>
                        <p><strong>Telefone:</strong> {empresa.telefone_empresa or "-"}</p>
                        
                        <h3>Informações da Entrega:</h3>
                        <p><strong>Data de Registro:</strong> {entrega.data_registro}</p>
                        <p><strong>Hora de Registro:</strong> {entrega.hora_registro}</p>
                        <p><strong>Nota Fiscal:</strong> {entrega.nota_fiscal or "-"}</p>
                        <p><strong>Observações:</strong> {entrega.observacoes or "-"}</p>
                        <p><em>Email enviado em: {diaehoradeenvio}</em></p>
                        
                        <p>Esta entrega possui {imagens_count} imagens anexadas a este email.</p>
                        
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                            Este é um email automático enviado pelo sistema VigiAPP. Favor não responder.
                        </p>
                    </body>
                    </html>
                    """
        
        # Log das imagens sendo enviadas
        if imagens_paths:
            print(f"Anexando {len(imagens_paths)} imagens ao email:")
            for img in imagens_paths:
                print(f"  - {img['filename']} ({img['type']})")
        else:
            print("Nenhuma imagem para anexar ao email.")
        
        # Envia o email com anexos
        return self.send_email(subject, html_content, attachments=imagens_paths)