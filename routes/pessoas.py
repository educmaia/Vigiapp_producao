from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session
)
from flask_login import login_required, current_user
from app import db
from models import Pessoa
from forms import PessoaForm
from utils import format_cpf, format_telefone
import re

pessoas_bp = Blueprint('pessoas', __name__, url_prefix='/pessoas')

@pessoas_bp.route('/')
@login_required
def index():
    pessoas = Pessoa.query.all()
    return render_template('pessoas/index.html', pessoas=pessoas)

@pessoas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = PessoaForm()
    
    if form.validate_on_submit():
        cpf = re.sub(r'[^0-9]', '', form.cpf.data)
        
        # Format CPF for storage
        formatted_cpf = format_cpf(cpf)
        
        # Check if CPF already exists
        existing_pessoa = Pessoa.query.filter_by(cpf=formatted_cpf).first()
        if existing_pessoa:
            flash('CPF já cadastrado.', 'danger')
            return render_template('pessoas/form.html', form=form, title='Novo Cadastro')
        
        # Format phone for storage
        telefone = format_telefone(form.telefone.data) if form.telefone.data else ""
        
        # Create new pessoa
        nova_pessoa = Pessoa(
            cpf=formatted_cpf,
            nome=form.nome.data,
            telefone=telefone,
            empresa=form.empresa.data
        )
        
        db.session.add(nova_pessoa)
        db.session.commit()
        
        flash('Pessoa cadastrada com sucesso!', 'success')
        
        # Usar session para armazenar as informações necessárias para o modal
        session['mostrar_oferta_ingresso'] = True
        session['pessoa_cpf'] = formatted_cpf
        session['pessoa_nome'] = form.nome.data
        
        # Enviar email de notificação
        from email_sender import EmailSender
        email_sender = EmailSender()
        email_sender.enviar_email_pessoa(
            cpf=formatted_cpf,
            nome=form.nome.data,
            telefone=telefone,
            empresa=form.empresa.data,
            motivo="",
            pessoa_setor="",
            observacoes=""
        )
        
        return redirect(url_for('pessoas.index'))
    
    return render_template('pessoas/form.html', form=form, title='Novo Cadastro')

@pessoas_bp.route('/editar/<string:cpf>', methods=['GET', 'POST'])
@login_required
def editar(cpf):
    pessoa = Pessoa.query.get_or_404(cpf)
    form = PessoaForm(obj=pessoa)
    
    if form.validate_on_submit():
        # Only admins can edit records
        if current_user.role != 'admin':
            flash('Apenas administradores podem editar registros.', 'danger')
            return redirect(url_for('pessoas.index'))
        
        new_cpf = format_cpf(form.cpf.data)
        
        # If CPF is being changed, check if new CPF already exists
        if new_cpf != cpf:
            existing_pessoa = Pessoa.query.filter_by(cpf=new_cpf).first()
            if existing_pessoa:
                flash('CPF já cadastrado.', 'danger')
                return render_template('pessoas/form.html', form=form, title='Editar Cadastro')
        
        # Update pessoa
        pessoa.cpf = new_cpf
        pessoa.nome = form.nome.data
        pessoa.telefone = format_telefone(form.telefone.data) if form.telefone.data else ""
        pessoa.empresa = form.empresa.data
        
        db.session.commit()
        
        flash('Cadastro atualizado com sucesso!', 'success')
        return redirect(url_for('pessoas.index'))
    
    return render_template('pessoas/form.html', form=form, title='Editar Cadastro')

@pessoas_bp.route('/excluir/<string:cpf>', methods=['POST'])
@login_required
def excluir(cpf):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('pessoas.index'))
    
    pessoa = Pessoa.query.get_or_404(cpf)
    
    try:
        db.session.delete(pessoa)
        db.session.commit()
        flash('Cadastro excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir pessoa: {str(e)}")
        flash('Não foi possível excluir este cadastro. Verifique se há registros vinculados.', 'danger')
    
    return redirect(url_for('pessoas.index'))

@pessoas_bp.route('/visualizar/<string:cpf>')
@login_required
def visualizar(cpf):
    """Visualiza os detalhes de uma pessoa específica"""
    pessoa = Pessoa.query.get_or_404(cpf)
    return render_template('pessoas/visualizar.html', pessoa=pessoa, title=f'Detalhes - {pessoa.nome}')

@pessoas_bp.route('/buscar-por-cpf/<string:cpf>')
@login_required
def buscar_por_cpf(cpf):
    formatted_cpf = format_cpf(cpf)
    pessoa = Pessoa.query.filter_by(cpf=formatted_cpf).first()
    
    if pessoa:
        return jsonify({
            'nome': pessoa.nome,
            'telefone': pessoa.telefone,
            'empresa': pessoa.empresa
        })
    
    return jsonify({}), 404

@pessoas_bp.route('/limpar-session', methods=['POST'])
@login_required
def limpar_session():
    # Limpar as variáveis de sessão usadas para o modal
    if 'mostrar_oferta_ingresso' in session:
        session.pop('mostrar_oferta_ingresso', None)
    if 'pessoa_cpf' in session:
        session.pop('pessoa_cpf', None)
    if 'pessoa_nome' in session:
        session.pop('pessoa_nome', None)
    
    return jsonify({"status": "success"})
