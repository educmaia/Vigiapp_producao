from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session
)
from flask_login import login_required, current_user
from app import db
from models import Empresa
from forms import EmpresaForm
from utils import format_cnpj, format_telefone
import re

empresas_bp = Blueprint('empresas', __name__, url_prefix='/empresas')

@empresas_bp.route('/')
@login_required
def index():
    empresas = Empresa.query.all()
    return render_template('empresas/index.html', empresas=empresas)

@empresas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = EmpresaForm()
    
    if form.validate_on_submit():
        cnpj = re.sub(r'[^0-9]', '', form.cnpj.data)
        
        # Format CNPJ for storage
        formatted_cnpj = format_cnpj(cnpj)
        
        # Check if CNPJ already exists
        existing_empresa = Empresa.query.filter_by(cnpj=formatted_cnpj).first()
        if existing_empresa:
            flash('CNPJ já cadastrado.', 'danger')
            return render_template('empresas/form.html', form=form, title='Nova Empresa')
        
        # Format phone numbers for storage
        telefone_empresa = format_telefone(form.telefone_empresa.data) if form.telefone_empresa.data else ""
        telefone_func = format_telefone(form.telefone_func.data) if form.telefone_func.data else ""
        
        # Create new empresa
        nova_empresa = Empresa(
            cnpj=formatted_cnpj,
            nome_empresa=form.nome_empresa.data,
            telefone_empresa=telefone_empresa,
            coringa=form.coringa.data,
            nome_func=form.nome_func.data,
            telefone_func=telefone_func
        )
        
        db.session.add(nova_empresa)
        db.session.commit()
        
        flash('Empresa cadastrada com sucesso!', 'success')
        
        # Usar session para armazenar as informações necessárias para o modal
        session['mostrar_oferta_entrega'] = True
        session['empresa_cnpj'] = formatted_cnpj
        session['empresa_nome'] = form.nome_empresa.data
        
        return redirect(url_for('empresas.index'))
    
    return render_template('empresas/form.html', form=form, title='Nova Empresa')

@empresas_bp.route('/editar/<string:cnpj>', methods=['GET', 'POST'])
@login_required
def editar(cnpj):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('empresas.index'))
    
    empresa = Empresa.query.get_or_404(cnpj)
    form = EmpresaForm(obj=empresa)
    
    if form.validate_on_submit():
        new_cnpj = format_cnpj(form.cnpj.data)
        
        # If CNPJ is being changed, check if new CNPJ already exists
        if new_cnpj != cnpj:
            existing_empresa = Empresa.query.filter_by(cnpj=new_cnpj).first()
            if existing_empresa:
                flash('CNPJ já cadastrado.', 'danger')
                return render_template('empresas/form.html', form=form, title='Editar Empresa')
        
        # Update empresa
        empresa.cnpj = new_cnpj
        empresa.nome_empresa = form.nome_empresa.data
        empresa.telefone_empresa = format_telefone(form.telefone_empresa.data) if form.telefone_empresa.data else ""
        empresa.coringa = form.coringa.data
        empresa.nome_func = form.nome_func.data
        empresa.telefone_func = format_telefone(form.telefone_func.data) if form.telefone_func.data else ""
        
        db.session.commit()
        
        flash('Empresa atualizada com sucesso!', 'success')
        return redirect(url_for('empresas.index'))
    
    return render_template('empresas/form.html', form=form, title='Editar Empresa')

@empresas_bp.route('/excluir/<string:cnpj>', methods=['POST'])
@login_required
def excluir(cnpj):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('empresas.index'))
    
    empresa = Empresa.query.get_or_404(cnpj)
    
    try:
        db.session.delete(empresa)
        db.session.commit()
        flash('Empresa excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir empresa: {str(e)}")
        flash('Não foi possível excluir esta empresa. Verifique se há entregas vinculadas.', 'danger')
    
    return redirect(url_for('empresas.index'))

@empresas_bp.route('/buscar-por-cnpj/<string:cnpj>')
@login_required
def buscar_por_cnpj(cnpj):
    formatted_cnpj = format_cnpj(cnpj)
    empresa = Empresa.query.filter_by(cnpj=formatted_cnpj).first()
    
    if empresa:
        return jsonify({
            'nome_empresa': empresa.nome_empresa,
            'telefone_empresa': empresa.telefone_empresa,
            'coringa': empresa.coringa,
            'nome_func': empresa.nome_func,
            'telefone_func': empresa.telefone_func
        })
    
    return jsonify({}), 404

@empresas_bp.route('/limpar-session', methods=['POST'])
@login_required
def limpar_session():
    # Limpar as variáveis de sessão usadas para o modal
    if 'mostrar_oferta_entrega' in session:
        session.pop('mostrar_oferta_entrega', None)
    if 'empresa_cnpj' in session:
        session.pop('empresa_cnpj', None)
    if 'empresa_nome' in session:
        session.pop('empresa_nome', None)
    
    return jsonify({"status": "success"})
