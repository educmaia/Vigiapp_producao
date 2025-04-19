from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db
from models import User
from forms import EditUserForm, ChangePasswordForm

# Blueprint para gerenciamento de usuários
users_bp = Blueprint('users', __name__)

@users_bp.route('/gerenciar', methods=['GET'])
@login_required
def manage():
    """Exibe lista de usuários para gerenciamento (apenas admin)"""
    # Verifica se o usuário atual é administrador
    if current_user.role != 'admin':
        flash('Acesso negado. Somente administradores podem acessar esta página.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    # Busca todos os usuários
    users = User.query.order_by(User.username).all()
    
    return render_template('users/manage.html', users=users)

@users_bp.route('/editar/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    """Edita um usuário existente"""
    # Verifica se o usuário atual é administrador
    if current_user.role != 'admin':
        flash('Acesso negado. Somente administradores podem acessar esta página.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    # Busca o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Não permite editar o próprio usuário administrador (para evitar auto-degradação)
    if user.id == current_user.id:
        flash('Não é possível editar seu próprio usuário por esta tela.', 'warning')
        return redirect(url_for('users.manage'))
    
    # Cria e preenche o formulário com os dados do usuário
    form = EditUserForm()
    
    if form.validate_on_submit():
        # Verificar se o nome de usuário já existe (para outro usuário)
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.id != user_id:
            flash('Nome de usuário já está em uso. Escolha outro nome.', 'danger')
            return render_template('users/edit.html', form=form, user=user)
        
        # Verificar se o email já existe (para outro usuário)
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email and existing_email.id != user_id:
            flash('Email já está em uso. Escolha outro email.', 'danger')
            return render_template('users/edit.html', form=form, user=user)
        
        # Atualiza os dados do usuário
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.active = form.active.data == '1'  # Converte valor do select para boolean
        
        # Salva as alterações no banco de dados
        db.session.commit()
        
        flash(f'Usuário {user.username} atualizado com sucesso!', 'success')
        return redirect(url_for('users.manage'))
    
    # Preenche o formulário com os dados do usuário
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
        form.active.data = '1' if user.active else '0'
    
    return render_template('users/edit.html', form=form, user=user)

@users_bp.route('/alterar-senha/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """Altera a senha de um usuário"""
    # Verifica se o usuário atual é administrador
    if current_user.role != 'admin':
        flash('Acesso negado. Somente administradores podem acessar esta página.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    # Busca o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Cria o formulário
    form = ChangePasswordForm()
    
    # Para administradores, a senha atual não é necessária quando alterando a senha de outro usuário
    if user.id != current_user.id:
        form.current_password.validators = []
    
    if form.validate_on_submit():
        # Se for o próprio usuário, verifica a senha atual
        if user.id == current_user.id:
            if not check_password_hash(user.password_hash, form.current_password.data):
                flash('Senha atual incorreta.', 'danger')
                return render_template('users/change_password.html', form=form, user=user)
        
        # Atualiza a senha
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        
        flash(f'Senha do usuário {user.username} alterada com sucesso!', 'success')
        return redirect(url_for('users.manage'))
    
    return render_template('users/change_password.html', form=form, user=user)

@users_bp.route('/excluir/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    """Exclui um usuário"""
    # Verifica se o usuário atual é administrador
    if current_user.role != 'admin':
        flash('Acesso negado. Somente administradores podem acessar esta página.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    # Busca o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Não permite excluir o próprio usuário
    if user.id == current_user.id:
        flash('Não é possível excluir seu próprio usuário.', 'danger')
        return redirect(url_for('users.manage'))
    
    # Armazena o nome do usuário para mensagem
    username = user.username
    
    # Exclui o usuário
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuário {username} excluído com sucesso.', 'success')
    return redirect(url_for('users.manage'))