from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app,
    send_from_directory, session
)
from flask_login import login_required, current_user
from app import db
from models import Entrega, Empresa, EntregaImagem, ImagemEntrega
from forms import EntregaForm
from utils import get_brasil_datetime, format_cnpj
import re
import os
import io
from werkzeug.utils import secure_filename
from PIL import Image
from flask_wtf.csrf import validate_csrf

entregas_bp = Blueprint('entregas', __name__, url_prefix='/entregas', static_folder='static')

# Configuração para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/uploads/entregas')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Criar diretório de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(img_file, target_size=(800, 600)):
    """
    Redimensiona a imagem para o tamanho alvo, mantendo a proporção.
    
    Args:
        img_file: O arquivo de imagem como um objeto file-like
        target_size: Tupla com (largura, altura) desejadas
        
    Returns:
        BytesIO com a imagem redimensionada
    """
    img = Image.open(img_file)
    
    # Determinar orientação da imagem
    width, height = img.size
    if width > height:
        # Imagem horizontal
        target_size = (800, 600)
    else:
        # Imagem vertical
        target_size = (600, 800)
        
    # Calcular nova proporção mantendo a relação de aspecto
    img_ratio = width / height
    target_ratio = target_size[0] / target_size[1]
    
    if img_ratio > target_ratio:
        # Imagem mais larga que o alvo
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)
    else:
        # Imagem mais alta que o alvo
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)
    
    # Redimensionar a imagem
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Salvar em um buffer de memória
    img_io = io.BytesIO()
    
    # Determinar formato de saída baseado no formato original
    if img.format:
        format = img.format
    else:
        format = 'JPEG'  # Padrão para formato desconhecido
    
    # Otimizar e salvar
    if format == 'JPEG':
        resized_img.save(img_io, format=format, quality=85, optimize=True)
    else:
        resized_img.save(img_io, format=format, optimize=True)
    
    img_io.seek(0)
    return img_io

@entregas_bp.route('/')
@login_required
def index():
    entregas = Entrega.query.order_by(Entrega.data_registro.desc(), Entrega.hora_registro.desc()).all()
    return render_template('entregas/index.html', entregas=entregas)

@entregas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = EntregaForm()
    
    # Pre-fill date and time if not submitted
    if request.method == 'GET':
        current_time = get_brasil_datetime()
        form.data_registro.data = current_time.strftime('%d/%m/%Y')
        form.hora_registro.data = current_time.strftime('%H:%M')
        form.data_envio.data = current_time.strftime('%d/%m/%Y')
        form.hora_envio.data = current_time.strftime('%H:%M')
        
        # Pre-fill CNPJ if provided in URL params
        cnpj_param = request.args.get('cnpj')
        if cnpj_param:
            form.cnpj.data = cnpj_param
    
    if form.validate_on_submit():
        cnpj = re.sub(r'[^0-9]', '', form.cnpj.data)
        formatted_cnpj = format_cnpj(cnpj)
        
        # Check if company exists
        empresa = Empresa.query.filter_by(cnpj=formatted_cnpj).first()
        if not empresa:
            flash('CNPJ não cadastrado. Cadastre a empresa primeiro.', 'danger')
            return render_template('entregas/form.html', form=form, title='Nova Entrega')
        
        # Get current time in Brazil timezone using our helper function
        current_time = get_brasil_datetime()
        
        # Format current date and time
        data_atual = current_time.strftime('%d/%m/%Y')
        hora_atual = current_time.strftime('%H:%M')
        
        # Mensagem padrão
        flash_message = "Entrega registrada com sucesso!"
        
        # Create new entrega
        nova_entrega = Entrega(
            cnpj=formatted_cnpj,
            data_registro=data_atual,
            hora_registro=hora_atual,
            data_envio=data_atual,  # Set delivery date same as registration
            hora_envio=hora_atual,  # Set delivery time same as registration
            nota_fiscal=form.nota_fiscal.data,
            observacoes=form.observacoes.data,
            imagem_filename=None
        )
        
        db.session.add(nova_entrega)
        db.session.commit()
        
        # Processar upload de múltiplas imagens
        if form.imagens.data and form.imagens.data[0]:
            for i, imagem in enumerate(form.imagens.data):
                if imagem and allowed_file(imagem.filename):
                    # Usar ID da entrega, índice e timestamp para criar um nome único
                    timestamp = get_brasil_datetime().strftime('%Y%m%d%H%M%S')
                    filename = secure_filename(f"{nova_entrega.id}_{timestamp}_{i}_{imagem.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    
                    # Redimensionar e salvar a imagem
                    imagem.seek(0)  # Garantir que estamos no início do arquivo
                    img_io = resize_image(imagem)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_io.getbuffer())
                    
                    # Criar registro de imagem para esta entrega
                    nova_imagem = EntregaImagem(
                        entrega_id=nova_entrega.id,
                        filename=filename
                    )
                    db.session.add(nova_imagem)
            
            # Commit todas as imagens de uma vez
            db.session.commit()
            
            # Enviar email com anexos
            try:
                # Buscar empresa relacionada a esta entrega
                empresa = Empresa.query.filter_by(cnpj=nova_entrega.cnpj).first()
                
                # Preparar informações de anexos para o email
                email_imagens = []
                for imagem in nova_entrega.imagens:
                    imagem_path = os.path.join(UPLOAD_FOLDER, imagem.filename)
                    if os.path.exists(imagem_path):
                        mime_type = "image/jpeg"  # Default MIME type
                        if imagem.filename.lower().endswith('.png'):
                            mime_type = "image/png"
                        
                        email_imagens.append({
                            'filepath': imagem_path,
                            'filename': imagem.filename,
                            'type': mime_type
                        })
                
                # Enviar email usando a instância global do email_sender
                from app import email_sender
                success, response = email_sender.enviar_email_entrega(
                    entrega=nova_entrega, 
                    empresa=empresa, 
                    imagens_paths=email_imagens
                )
                
                if success:
                    current_app.logger.info(f"Email enviado com sucesso para entrega ID {nova_entrega.id}")
                    flash_message = "Entrega registrada com sucesso! Um e-mail de notificação foi enviado."
                else:
                    current_app.logger.warning(f"Falha ao enviar email para entrega ID {nova_entrega.id}: {response}")
                    flash_message = "Entrega registrada com sucesso! Nota: Não foi possível enviar o e-mail de notificação."
            except Exception as e:
                current_app.logger.error(f"Erro ao enviar email: {str(e)}")
                flash_message = "Entrega registrada com sucesso! Nota: Houve um erro ao tentar enviar o e-mail de notificação."
        else:
            # Se não há imagens, não tenta enviar e-mail
            flash_message = "Entrega registrada com sucesso!"
        
        flash(flash_message, 'success')
        return redirect(url_for('entregas.index'))
    
    return render_template('entregas/form.html', form=form, title='Nova Entrega')

@entregas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('entregas.index'))
    
    entrega = Entrega.query.get_or_404(id)
    form = EntregaForm(obj=entrega)
    
    if form.validate_on_submit():
        cnpj = re.sub(r'[^0-9]', '', form.cnpj.data)
        formatted_cnpj = format_cnpj(cnpj)
        
        # Check if company exists
        empresa = Empresa.query.filter_by(cnpj=formatted_cnpj).first()
        if not empresa:
            flash('CNPJ não cadastrado. Cadastre a empresa primeiro.', 'danger')
            return render_template('entregas/form.html', form=form, title='Editar Entrega', entrega=entrega)
        
        # Update entrega
        entrega.cnpj = formatted_cnpj
        entrega.data_registro = form.data_registro.data
        entrega.hora_registro = form.hora_registro.data
        entrega.data_envio = form.data_envio.data
        entrega.hora_envio = form.hora_envio.data
        entrega.nota_fiscal = form.nota_fiscal.data
        entrega.observacoes = form.observacoes.data
        
        db.session.commit()
        
        # Processar upload de múltiplas imagens
        if form.imagens.data and form.imagens.data[0]:
            for i, imagem in enumerate(form.imagens.data):
                if imagem and allowed_file(imagem.filename):
                    # Usar ID da entrega, índice e timestamp para criar um nome único
                    timestamp = get_brasil_datetime().strftime('%Y%m%d%H%M%S')
                    filename = secure_filename(f"{entrega.id}_{timestamp}_{i}_{imagem.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    
                    # Redimensionar e salvar a imagem
                    imagem.seek(0)  # Garantir que estamos no início do arquivo
                    img_io = resize_image(imagem)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_io.getbuffer())
                    
                    # Criar registro de imagem para esta entrega
                    nova_imagem = EntregaImagem(
                        entrega_id=entrega.id,
                        filename=filename
                    )
                    db.session.add(nova_imagem)
            
            # Commit todas as imagens de uma vez
            db.session.commit()
        
        flash('Entrega atualizada com sucesso!', 'success')
        return redirect(url_for('entregas.index'))
    
    return render_template('entregas/form.html', form=form, title='Editar Entrega', entrega=entrega)

@entregas_bp.route('/registrar-envio/<int:id>', methods=['POST'])
@login_required
def registrar_envio(id):
    entrega = Entrega.query.get_or_404(id)
    
    if entrega.data_envio and entrega.hora_envio:
        flash('Envio já registrado para esta entrega.', 'warning')
    else:
        now = get_brasil_datetime()
        entrega.data_envio = now.strftime('%d/%m/%Y')
        entrega.hora_envio = now.strftime('%H:%M')
        db.session.commit()
        flash('Envio registrado com sucesso!', 'success')
    
    return redirect(url_for('entregas.index'))

@entregas_bp.route('/confirmar-exclusao/<int:id>')
@login_required
def confirmar_exclusao(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('entregas.index'))
    
    entrega = Entrega.query.get_or_404(id)
    empresa = Empresa.query.get(entrega.cnpj)
    
    # Renderiza a página de confirmação de exclusão
    return render_template(
        'entregas/confirmar_exclusao.html',
        entrega=entrega,
        empresa=empresa,
        action_url=url_for('entregas.excluir', id=id),
        cancel_url=url_for('entregas.index')
    )

@entregas_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('entregas.index'))
    
    entrega = Entrega.query.get_or_404(id)
    
    try:
        # Excluir todas as imagens associadas
        for imagem in entrega.imagens:
            try:
                if os.path.exists(os.path.join(UPLOAD_FOLDER, imagem.filename)):
                    os.remove(os.path.join(UPLOAD_FOLDER, imagem.filename))
            except Exception as e:
                current_app.logger.error(f"Erro ao excluir arquivo de imagem: {str(e)}")
                flash(f'Erro ao excluir imagem: {str(e)}', 'warning')
        
        # Excluir imagem antiga se existir (para compatibilidade)
        if entrega.imagem_filename:
            try:
                if os.path.exists(os.path.join(UPLOAD_FOLDER, entrega.imagem_filename)):
                    os.remove(os.path.join(UPLOAD_FOLDER, entrega.imagem_filename))
            except Exception as e:
                current_app.logger.error(f"Erro ao excluir imagem antiga: {str(e)}")
                pass
        
        db.session.delete(entrega)
        db.session.commit()
        flash('Entrega excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir entrega: {str(e)}")
        flash(f'Erro ao excluir entrega: {str(e)}', 'danger')
    
    return redirect(url_for('entregas.index'))

@entregas_bp.route('/imagem/<filename>')
@login_required
def imagem(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@entregas_bp.route('/excluir-imagem/<int:id>', methods=['POST'])
@login_required
def excluir_imagem(id):
    # Only admins can delete images
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir imagens.', 'danger')
        return redirect(url_for('entregas.index'))
    
    imagem = EntregaImagem.query.get_or_404(id)
    entrega_id = imagem.entrega_id
    
    # Excluir o arquivo de imagem
    if os.path.exists(os.path.join(UPLOAD_FOLDER, imagem.filename)):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, imagem.filename))
        except Exception as e:
            flash(f'Erro ao excluir arquivo de imagem: {str(e)}', 'warning')
    
    # Excluir o registro da imagem
    db.session.delete(imagem)
    db.session.commit()
    
    flash('Imagem excluída com sucesso!', 'success')
    return redirect(url_for('entregas.editar', id=entrega_id))
