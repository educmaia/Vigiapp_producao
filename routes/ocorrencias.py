from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_required, current_user
from app import db
from models import Ocorrencia
from forms import OcorrenciaForm
from datetime import datetime
from email_sender import EmailSender

ocorrencias_bp = Blueprint('ocorrencias', __name__, url_prefix='/ocorrencias')

@ocorrencias_bp.route('/')
@login_required
def index():
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.data_registro.desc()).all()
    return render_template('ocorrencias/index.html', ocorrencias=ocorrencias)

@ocorrencias_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = OcorrenciaForm()
    
    # Pre-fill date, time and vigilante if not submitted
    if request.method == 'GET':
        today = datetime.now()
        form.data_registro.data = today.date()
        form.hora_registro.data = today.time()
        form.vigilante.data = current_user.username
    
    if form.validate_on_submit():
        # Create new ocorrencia
        nova_ocorrencia = Ocorrencia(
            vigilante=form.vigilante.data,
            envolvidos=form.envolvidos.data,
            data_registro=form.data_registro.data,
            hora_registro=form.hora_registro.data,
            gravidade=form.gravidade.data,
            ocorrencia=form.ocorrencia.data
        )
        
        db.session.add(nova_ocorrencia)
        db.session.commit()
        
        # Send email notification
        try:
            email_sender = EmailSender()
            success, response = email_sender.enviar_email_ocorrencia(
                form.vigilante.data,
                form.envolvidos.data,
                form.data_registro.data.strftime('%d/%m/%Y'),
                form.hora_registro.data.strftime('%H:%M'),
                form.gravidade.data,
                form.ocorrencia.data
            )
            
            if success:
                current_app.logger.info("Email enviado com sucesso")
            else:
                current_app.logger.warning(f"Falha ao enviar email: {response}")
                
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar email: {str(e)}")
        
        flash('Ocorrência registrada com sucesso!', 'success')
        return redirect(url_for('ocorrencias.index'))
    
    return render_template('ocorrencias/form.html', form=form, title='Nova Ocorrência')

@ocorrencias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('ocorrencias.index'))
    
    ocorrencia = Ocorrencia.query.get_or_404(id)
    form = OcorrenciaForm(obj=ocorrencia)
    
    if form.validate_on_submit():
        # Update ocorrencia
        ocorrencia.vigilante = form.vigilante.data
        ocorrencia.envolvidos = form.envolvidos.data
        ocorrencia.data_registro = form.data_registro.data
        ocorrencia.hora_registro = form.hora_registro.data
        ocorrencia.gravidade = form.gravidade.data
        ocorrencia.ocorrencia = form.ocorrencia.data
        
        db.session.commit()
        flash('Ocorrência atualizada com sucesso!', 'success')
        return redirect(url_for('ocorrencias.index'))
    
    return render_template('ocorrencias/form.html', form=form, title='Editar Ocorrência')

@ocorrencias_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('ocorrencias.index'))
    
    ocorrencia = Ocorrencia.query.get_or_404(id)
    
    db.session.delete(ocorrencia)
    db.session.commit()
    
    flash('Ocorrência excluída com sucesso!', 'success')
    return redirect(url_for('ocorrencias.index'))
