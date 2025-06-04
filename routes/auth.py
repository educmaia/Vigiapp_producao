from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from models import User
from forms import LoginForm, RegisterForm
from security_monitor import security_monitor
from rate_limiter import rate_limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Verificar rate limiting
        ip_address = request.remote_addr
        if rate_limiter.is_blocked(ip_address):
            block_time = rate_limiter.get_block_time_remaining(ip_address)
            minutes = block_time // 60
            seconds = block_time % 60
            flash(f'Muitas tentativas de login. Tente novamente em {minutes} minutos e {seconds} segundos.', 'danger')
            return render_template('login.html', form=form)
        
        user = User.query.filter_by(username=form.username.data).first()
        
        # Registrar tentativa de login
        success = user and check_password_hash(user.password_hash, form.password.data)
        rate_limiter.record_attempt(ip_address, success)
        
        # Monitorar tentativa de login
        security_monitor.monitor_login_attempt(
            username=form.username.data,
            ip_address=ip_address,
            success=success
        )
        
        if success:
            if not user.active:
                flash('Sua conta está desativada. Entre em contato com o administrador.', 'danger')
                return render_template('login.html', form=form)
            
            # Atualizar o último login
            from datetime import datetime
            user.last_login = datetime.now()
            db.session.commit()
            
            # Realizar login
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page or url_for('auth.dashboard'))
        else:
            attempts = rate_limiter.get_attempts_count(ip_address)
            remaining = rate_limiter.max_attempts - attempts
            flash(f'Usuário ou senha inválidos. Tentativas restantes: {remaining}', 'danger')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Only admins can register new users
    if current_user.role != 'admin':
        flash('Acesso negado. Apenas administradores podem registrar novos usuários.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Nome de usuário já existe. Escolha outro.', 'danger')
            return render_template('register.html', form=form)
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email já cadastrado. Use outro email.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'Usuário {form.username.data} criado com sucesso!', 'success')
        return redirect(url_for('auth.dashboard'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')
