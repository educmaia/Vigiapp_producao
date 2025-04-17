from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_required, current_user
from app import db
from models import Ingresso, Pessoa
from forms import IngressoForm
from utils import get_brasil_datetime
from utils import format_cpf
from email_sender import EmailSender
import re

ingressos_bp = Blueprint('ingressos', __name__, url_prefix='/ingressos')

@ingressos_bp.route('/')
@login_required
def index():
    ingressos = Ingresso.query.order_by(Ingresso.data.desc(), Ingresso.entrada.desc()).all()
    return render_template('ingressos/index.html', ingressos=ingressos)

@ingressos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = IngressoForm()
    
    # Pre-fill date and time if not submitted with Brazil timezone
    if request.method == 'GET':
        today = get_brasil_datetime()
        form.data.data = today.strftime('%d/%m/%Y')
        form.entrada.data = today.strftime('%H:%M')
    
    if form.validate_on_submit():
        cpf = re.sub(r'[^0-9]', '', form.cpf.data)
        formatted_cpf = format_cpf(cpf)
        
        # Check if person exists
        pessoa = Pessoa.query.filter_by(cpf=formatted_cpf).first()
        if not pessoa:
            flash('CPF não cadastrado. Cadastre a pessoa primeiro.', 'danger')
            return render_template('ingressos/form.html', form=form, title='Novo Ingresso')
        
        # Create new ingresso
        novo_ingresso = Ingresso(
            cpf=formatted_cpf,
            data=form.data.data,
            entrada=form.entrada.data,
            saida=form.saida.data,
            motivo=form.motivo.data,
            pessoa_setor=form.pessoa_setor.data,
            observacoes=form.observacoes.data
        )
        
        db.session.add(novo_ingresso)
        db.session.commit()
        
        # Send email notification
        try:
            email_sender = EmailSender()
            
            # Enviar email usando o novo método específico para ingressos
            success, response = email_sender.enviar_email_ingresso(
                ingresso=novo_ingresso,
                pessoa=pessoa
            )
            
            if success:
                current_app.logger.info(f"Email enviado com sucesso para ingresso ID {novo_ingresso.id}")
            else:
                current_app.logger.warning(f"Falha ao enviar email para ingresso ID {novo_ingresso.id}: {response}")
                
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar email: {str(e)}")
        
        flash('Ingresso registrado com sucesso!', 'success')
        return redirect(url_for('ingressos.index'))
    
    return render_template('ingressos/form.html', form=form, title='Novo Ingresso')

@ingressos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('ingressos.index'))
    
    ingresso = Ingresso.query.get_or_404(id)
    form = IngressoForm(obj=ingresso)
    
    if form.validate_on_submit():
        cpf = re.sub(r'[^0-9]', '', form.cpf.data)
        formatted_cpf = format_cpf(cpf)
        
        # Check if person exists
        pessoa = Pessoa.query.filter_by(cpf=formatted_cpf).first()
        if not pessoa:
            flash('CPF não cadastrado. Cadastre a pessoa primeiro.', 'danger')
            return render_template('ingressos/form.html', form=form, title='Editar Ingresso')
        
        # Update ingresso
        ingresso.cpf = formatted_cpf
        ingresso.data = form.data.data
        ingresso.entrada = form.entrada.data
        ingresso.saida = form.saida.data
        ingresso.motivo = form.motivo.data
        ingresso.pessoa_setor = form.pessoa_setor.data
        ingresso.observacoes = form.observacoes.data
        
        db.session.commit()
        flash('Ingresso atualizado com sucesso!', 'success')
        return redirect(url_for('ingressos.index'))
    
    return render_template('ingressos/form.html', form=form, title='Editar Ingresso')

@ingressos_bp.route('/registrar-saida/<int:id>', methods=['POST'])
@login_required
def registrar_saida(id):
    ingresso = Ingresso.query.get_or_404(id)
    
    if ingresso.saida:
        flash('Saída já registrada para este ingresso.', 'warning')
    else:
        now = get_brasil_datetime()
        ingresso.saida = now.strftime('%H:%M')
        db.session.commit()
        flash('Saída registrada com sucesso!', 'success')
    
    return redirect(url_for('ingressos.index'))

@ingressos_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('ingressos.index'))
    
    ingresso = Ingresso.query.get_or_404(id)
    
    db.session.delete(ingresso)
    db.session.commit()
    
    flash('Ingresso excluído com sucesso!', 'success')
    return redirect(url_for('ingressos.index'))
