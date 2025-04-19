from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_required, current_user
from app import db, email_sender
from models import Correspondencia
from forms import CorrespondenciaForm
from utils import get_brasil_datetime

correspondencias_bp = Blueprint('correspondencias', __name__, url_prefix='/correspondencias')

@correspondencias_bp.route('/')
@login_required
def index():
    correspondencias = Correspondencia.query.order_by(Correspondencia.data_recebimento.desc()).all()
    return render_template('correspondencias/index.html', correspondencias=correspondencias)

@correspondencias_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = CorrespondenciaForm()
    
    # Pre-fill date and time if not submitted with Brazil timezone
    if request.method == 'GET':
        today = get_brasil_datetime()
        form.data_recebimento.data = today.date()
        form.hora_recebimento.data = today.time()
    
    if form.validate_on_submit():
        # Create new correspondencia
        nova_correspondencia = Correspondencia(
            remetente=form.remetente.data,
            destinatario=form.destinatario.data,
            data_recebimento=form.data_recebimento.data,
            hora_recebimento=form.hora_recebimento.data,
            data_destinacao=form.data_destinacao.data,
            hora_destinacao=form.hora_destinacao.data,
            tipo=form.tipo.data,
            setor_encomenda=form.setor_encomenda.data,
            observacoes=form.observacoes.data
        )
        
        db.session.add(nova_correspondencia)
        db.session.commit()
        
        # Send email notification
        try:
            # Usar instância global de email_sender
            success, response = email_sender.enviar_email_correspondencia(
                form.remetente.data,
                form.destinatario.data,
                form.tipo.data,
                form.setor_encomenda.data,
                form.data_recebimento.data.strftime('%d/%m/%Y'),
                form.hora_recebimento.data.strftime('%H:%M')
            )
            
            if success:
                current_app.logger.info(f"Email enviado com sucesso para correspondência ID {nova_correspondencia.id_correspondencia}")
            else:
                current_app.logger.warning(f"Falha ao enviar email para correspondência ID {nova_correspondencia.id_correspondencia}: {response}")
                
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar email: {str(e)}")
        
        flash('Correspondência registrada com sucesso!', 'success')
        return redirect(url_for('correspondencias.index'))
    
    return render_template('correspondencias/form.html', form=form, title='Nova Correspondência')

@correspondencias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('correspondencias.index'))
    
    correspondencia = Correspondencia.query.get_or_404(id)
    form = CorrespondenciaForm(obj=correspondencia)
    
    if form.validate_on_submit():
        # Update correspondencia
        correspondencia.remetente = form.remetente.data
        correspondencia.destinatario = form.destinatario.data
        correspondencia.data_recebimento = form.data_recebimento.data
        correspondencia.hora_recebimento = form.hora_recebimento.data
        correspondencia.data_destinacao = form.data_destinacao.data
        correspondencia.hora_destinacao = form.hora_destinacao.data
        correspondencia.tipo = form.tipo.data
        correspondencia.setor_encomenda = form.setor_encomenda.data
        correspondencia.observacoes = form.observacoes.data
        
        db.session.commit()
        flash('Correspondência atualizada com sucesso!', 'success')
        return redirect(url_for('correspondencias.index'))
    
    return render_template('correspondencias/form.html', form=form, title='Editar Correspondência')

@correspondencias_bp.route('/registrar-destinacao/<int:id>', methods=['POST'])
@login_required
def registrar_destinacao(id):
    correspondencia = Correspondencia.query.get_or_404(id)
    
    if correspondencia.data_destinacao and correspondencia.hora_destinacao:
        flash('Destinação já registrada para esta correspondência.', 'warning')
    else:
        now = get_brasil_datetime()
        correspondencia.data_destinacao = now.date()
        correspondencia.hora_destinacao = now.time()
        db.session.commit()
        flash('Destinação registrada com sucesso!', 'success')
    
    return redirect(url_for('correspondencias.index'))

@correspondencias_bp.route('/confirmar-exclusao/<int:id>')
@login_required
def confirmar_exclusao(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('correspondencias.index'))
    
    correspondencia = Correspondencia.query.get_or_404(id)
    
    # Renderiza a página de confirmação de exclusão
    return render_template(
        'correspondencias/confirmar_exclusao.html',
        correspondencia=correspondencia,
        action_url=url_for('correspondencias.excluir', id=id),
        cancel_url=url_for('correspondencias.index')
    )

@correspondencias_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('correspondencias.index'))
    
    correspondencia = Correspondencia.query.get_or_404(id)
    
    try:
        db.session.delete(correspondencia)
        db.session.commit()
        flash('Correspondência excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir correspondência: {str(e)}")
        flash(f'Erro ao excluir correspondência: {str(e)}', 'danger')
    
    return redirect(url_for('correspondencias.index'))
