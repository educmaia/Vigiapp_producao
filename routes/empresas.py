from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session
)
from flask_login import login_required, current_user
from app import db
from models import Empresa, Entrega
from forms import EmpresaForm
from utils import format_cnpj, format_telefone
import re

# Criar um novo blueprint para empresas com configuração limpa
empresas_bp = Blueprint('empresas', __name__, url_prefix='/empresas')

# Listar todas as empresas
@empresas_bp.route('/')
@login_required
def index():
    busca = request.args.get('busca', '').strip()
    
    if busca:
        # Remove caracteres especiais do termo de busca para comparação de CNPJ
        busca_cnpj = re.sub(r'[^0-9]', '', busca)
        
        # Buscar por CNPJ ou nome da empresa
        empresas = Empresa.query.filter(
            db.or_(
                # Busca por CNPJ (com formatação)
                Empresa.cnpj.like(f'%{busca}%'),
                # Busca por CNPJ sem formatação
                db.func.replace(db.func.replace(db.func.replace(Empresa.cnpj, '.', ''), '-', ''), '/', '').like(f'%{busca_cnpj}%'),
                # Busca por nome da empresa (case insensitive)
                Empresa.nome_empresa.ilike(f'%{busca}%')
            )
        ).order_by(Empresa.nome_empresa).all()
    else:
        empresas = Empresa.query.order_by(Empresa.nome_empresa).all()
    
    # Limpar a sessão após mostrar o modal
    if session.get('mostrar_oferta_entrega'):
        session.pop('mostrar_oferta_entrega', None)
        session.pop('empresa_cnpj', None)
        session.pop('empresa_nome', None)
    
    return render_template('empresas/index.html', empresas=empresas)

# Adicionar nova empresa
@empresas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    form = EmpresaForm()
    
    # Pre-fill CNPJ if provided in URL parameters
    if request.method == 'GET':
        cnpj_param = request.args.get('cnpj')
        if cnpj_param:
            form.cnpj.data = cnpj_param
    
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

# Rota para editar empresa
@empresas_bp.route('/editar/<path:cnpj>', methods=['GET', 'POST'])
@empresas_bp.route('/editar-empresa/<path:cnpj>', methods=['GET', 'POST'])  # Rota alternativa para compatibilidade
@login_required
def editar(cnpj):
    # Only admins can edit records
    if current_user.role != 'admin':
        flash('Apenas administradores podem editar registros.', 'danger')
        return redirect(url_for('empresas.index'))
    
    empresa = Empresa.query.get_or_404(cnpj)
    
    # Pré-preencher o formulário com os dados atuais
    # Precisamos garantir que o CNPJ seja exibido exatamente como está no banco
    form = EmpresaForm(obj=empresa)
    
    if form.validate_on_submit():
        # Formatamos o CNPJ do formulário
        new_cnpj = format_cnpj(form.cnpj.data)
        
        try:
            # Se o CNPJ está sendo alterado, verificamos se o novo já existe
            if new_cnpj != cnpj:
                existing_empresa = Empresa.query.filter_by(cnpj=new_cnpj).first()
                if existing_empresa:
                    flash('CNPJ já cadastrado no sistema.', 'danger')
                    return render_template('empresas/form.html', form=form, title='Editar Empresa')
                
                # Aqui é um ponto crítico: precisamos criar uma nova empresa e transferir as entregas
                # em vez de apenas alterar o CNPJ, pois ele é a chave primária
                new_empresa = Empresa(
                    cnpj=new_cnpj,
                    nome_empresa=form.nome_empresa.data,
                    telefone_empresa=format_telefone(form.telefone_empresa.data) if form.telefone_empresa.data else "",
                    coringa=form.coringa.data,
                    nome_func=form.nome_func.data,
                    telefone_func=format_telefone(form.telefone_func.data) if form.telefone_func.data else ""
                )
                
                # Adicionamos a nova empresa
                db.session.add(new_empresa)
                
                # Atualizamos as entregas para usar o novo CNPJ
                for entrega in Entrega.query.filter_by(cnpj=cnpj).all():
                    entrega.cnpj = new_cnpj
                
                # Removemos a empresa antiga
                db.session.delete(empresa)
                
            else:
                # Se o CNPJ não mudou, atualizamos os demais campos normalmente
                empresa.nome_empresa = form.nome_empresa.data
                empresa.telefone_empresa = format_telefone(form.telefone_empresa.data) if form.telefone_empresa.data else ""
                empresa.coringa = form.coringa.data
                empresa.nome_func = form.nome_func.data
                empresa.telefone_func = format_telefone(form.telefone_func.data) if form.telefone_func.data else ""
            
            # Confirmamos as alterações
            db.session.commit()
            flash('Empresa atualizada com sucesso!', 'success')
            
        except Exception as e:
            # Em caso de erro, revertemos as alterações
            db.session.rollback()
            current_app.logger.error(f"Erro ao atualizar empresa: {str(e)}")
            flash(f'Erro ao atualizar empresa: {str(e)}', 'danger')
            return render_template('empresas/form.html', form=form, title='Editar Empresa')
        
        return redirect(url_for('empresas.index'))
    
    return render_template('empresas/form.html', form=form, title='Editar Empresa')

# Página de confirmação de exclusão
@empresas_bp.route('/confirmar-excluir/<path:cnpj>')
@empresas_bp.route('/confirmar_excluir/<path:cnpj>')  # Rota alternativa para compatibilidade
@login_required
def confirmar_excluir(cnpj):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('empresas.index'))
    
    empresa = Empresa.query.get_or_404(cnpj)
    
    # Contar entregas associadas a esta empresa
    entregas_count = Entrega.query.filter_by(cnpj=cnpj).count()
    
    # Renderiza a página de confirmação de exclusão
    return render_template(
        'empresas/confirmar_exclusao.html',
        empresa=empresa,
        entregas_count=entregas_count,
        action_url=url_for('empresas.executar_exclusao', cnpj=cnpj),
        cancel_url=url_for('empresas.index')
    )

# Executar a exclusão após confirmação
@empresas_bp.route('/executar-exclusao/<path:cnpj>', methods=['POST'])
@empresas_bp.route('/executar_exclusao/<path:cnpj>', methods=['POST'])  # Rota alternativa para compatibilidade
@login_required
def executar_exclusao(cnpj):
    # Only admins can delete records
    if current_user.role != 'admin':
        flash('Apenas administradores podem excluir registros.', 'danger')
        return redirect(url_for('empresas.index'))
    
    empresa = Empresa.query.get_or_404(cnpj)
    
    try:
        # Agora que configuramos o cascade, a exclusão de uma empresa deve automaticamente
        # excluir todas as entregas relacionadas, que por sua vez excluirão todas as imagens relacionadas
        
        # Log para debug
        current_app.logger.info(f"Excluindo empresa {empresa.nome_empresa} (CNPJ: {empresa.cnpj}) e {len(empresa.entregas)} entregas associadas")
        
        # Excluímos diretamente a empresa, confiando no CASCADE
        db.session.delete(empresa)
        db.session.commit()
        
        flash('Empresa excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir empresa: {str(e)}")
        flash('Não foi possível excluir esta empresa. Erro: ' + str(e), 'danger')
    
    return redirect(url_for('empresas.index'))

# Buscar informações de uma empresa através do CNPJ
@empresas_bp.route('/buscar-por-cnpj/<path:cnpj>')
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

# Limpar variáveis de sessão
@empresas_bp.route('/limpar-session', methods=['POST'])
@login_required
def limpar_session():
    session.pop('mostrar_oferta_entrega', None)
    session.pop('empresa_cnpj', None)
    session.pop('empresa_nome', None)
    return jsonify({'success': True})
