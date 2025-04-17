from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app,
    send_from_directory
)
from flask_login import login_required, current_user
from app import db
from models import Entrega, Empresa
from forms import EntregaForm
from datetime import datetime
from utils import format_cnpj
from email_sender import EmailSender
import re
import os
from werkzeug.utils import secure_filename

entregas_bp = Blueprint('entregas', __name__, url_prefix='/entregas', static_folder='static')

# Configuração para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/uploads/entregas')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Criar diretório de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        today = datetime.now()
        form.data_registro.data = today.strftime('%d/%m/%Y')
        form.hora_registro.data = today.strftime('%H:%M')
    
    if form.validate_on_submit():
        cnpj = re.sub(r'[^0-9]', '', form.cnpj.data)
        formatted_cnpj = format_cnpj(cnpj)
        
        # Check if company exists
        empresa = Empresa.query.filter_by(cnpj=formatted_cnpj).first()
        if not empresa:
            flash('CNPJ não cadastrado. Cadastre a empresa primeiro.', 'danger')
            return render_template('entregas/form.html', form=form, title='Nova Entrega')
        
        # Create new entrega
        nova_entrega = Entrega(
            cnpj=formatted_cnpj,
            data_registro=form.data_registro.data,
            hora_registro=form.hora_registro.data,
            data_envio=form.data_envio.data,
            hora_envio=form.hora_envio.data,
            nota_fiscal=form.nota_fiscal.data,
            observacoes=form.observacoes.data,
            imagem_filename=None
        )
        
        db.session.add(nova_entrega)
        db.session.commit()
        
        # Processar upload de imagem se fornecido
        if form.imagem.data:
            imagem = form.imagem.data
            if imagem and allowed_file(imagem.filename):
                # Usar ID da entrega e timestamp para criar um nome único
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = secure_filename(f"{nova_entrega.id}_{timestamp}_{imagem.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                imagem.save(filepath)
                
                # Atualizar a entrega com o nome do arquivo
                nova_entrega.imagem_filename = filename
                db.session.commit()
        
        flash('Entrega registrada com sucesso!', 'success')
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
        
        # Processar upload de imagem se fornecido
        if form.imagem.data:
            imagem = form.imagem.data
            if imagem and allowed_file(imagem.filename):
                # Remover imagem anterior se existir
                if entrega.imagem_filename and os.path.exists(os.path.join(UPLOAD_FOLDER, entrega.imagem_filename)):
                    try:
                        os.remove(os.path.join(UPLOAD_FOLDER, entrega.imagem_filename))
                    except:
                        pass
                
                # Usar ID da entrega e timestamp para criar um nome único
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = secure_filename(f"{entrega.id}_{timestamp}_{imagem.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                imagem.save(filepath)
                
                # Atualizar a entrega com o nome do arquivo
                entrega.imagem_filename = filename
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
        now = datetime.now()
        entrega.data_envio = now.strftime('%d/%m/%Y')
        entrega.hora_envio = now.strftime('%H:%M')
        db.session.commit()
        flash('Envio registrado com sucesso!', 'success')
    
    return redirect(url_for('entregas.index'))

@entregas_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('entregas.index'))
    
    entrega = Entrega.query.get_or_404(id)
    
    # Excluir imagem se existir
    if entrega.imagem_filename:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, entrega.imagem_filename))
        except:
            pass
    
    db.session.delete(entrega)
    db.session.commit()
    
    flash('Entrega excluída com sucesso!', 'success')
    return redirect(url_for('entregas.index'))

@entregas_bp.route('/imagem/<filename>')
@login_required
def imagem(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
