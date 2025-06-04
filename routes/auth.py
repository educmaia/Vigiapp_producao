from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from models import User
from forms import LoginForm, RegisterForm
from werkzeug.urls import url_parse
from datetime import datetime
from rate_limiter import rate_limiter
from security_monitor import security_monitor

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
    ip_address = request.remote_addr

    if rate_limiter.is_blocked(ip_address):
        block_time = rate_limiter.get_block_time_remaining(ip_address)
        minutes, seconds = divmod(block_time, 60)
        flash(f'Muitas tentativas de login. Tente novamente em {minutes} minutos e {seconds} segundos.', 'danger')
        return render_template('auth/login.html', form=form)

    if form.validate_on_submit():
        print(f"DEBUG: Antes da consulta ao DB. Usuário: {form.username.data}, IP: {ip_address}")
        user = User.query.filter_by(username=form.username.data).first()
        print(f"DEBUG: Após consulta ao DB. Usuário encontrado: {user.username if user else 'Nenhum'}")
        
        login_successful = False
        if user:
            print(f"DEBUG: Antes de user.check_password para {user.username}")
            login_successful = user.check_password(form.password.data)
            print(f"DEBUG: Após user.check_password. Sucesso: {login_successful}")
        else:
            print(f"DEBUG: Usuário {form.username.data} não encontrado no DB.")
        
        # Registrar tentativa com rate_limiter
        print(f"DEBUG: Antes de rate_limiter.record_attempt -- ESTA LINHA DEVE APARECER")
        # rate_limiter.record_attempt(ip_address, login_successful) # TEMPORARIAMENTE COMENTADO
        print(f"DEBUG: rate_limiter.record_attempt FOI COMENTADO")
        
        # Monitorar tentativa de login com security_monitor
        print(f"DEBUG: Antes de security_monitor.monitor_login_attempt -- ESTA LINHA DEVE APARECER")
        # security_monitor.monitor_login_attempt( # TEMPORARIAMENTE COMENTADO
        #     username=form.username.data,
        #     ip_address=ip_address,
        #     success=login_successful
        # )
        print(f"DEBUG: security_monitor.monitor_login_attempt FOI COMENTADO")
        
        if login_successful:
            print(f"Senha correta para usuário: {user.username}")
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('auth.dashboard')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page)
        else:
            print(f"Falha na autenticação para usuário: {form.username.data}")
            attempts = rate_limiter.get_attempts_count(ip_address)
            remaining_attempts = rate_limiter.max_attempts - attempts
            if rate_limiter.is_blocked(ip_address):
                 block_time = rate_limiter.get_block_time_remaining(ip_address)
                 minutes, seconds = divmod(block_time, 60)
                 flash(f'Muitas tentativas de login. Tente novamente em {minutes} minutos e {seconds} segundos.', 'danger')
            else:
                flash(f'Usuário ou senha inválidos. Tentativas restantes: {remaining_attempts}', 'danger')
    
    return render_template('auth/login.html', form=form)

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
