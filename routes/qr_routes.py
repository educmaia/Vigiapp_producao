from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Pessoa, Ingresso
from qr_code import generate_person_qr_code, generate_entrance_qr_code
from utils import get_brasil_datetime, format_cpf
import re

qr_bp = Blueprint('qr', __name__)

@qr_bp.route('/gerar-qrcode-pessoa/<cpf>')
@login_required
def gerar_qrcode_pessoa(cpf):
    """Gera ou recupera um código QR para uma pessoa"""
    # Normaliza o CPF
    cpf_normalizado = re.sub(r'[^0-9]', '', cpf)
    cpf_formatado = format_cpf(cpf_normalizado)
    
    # Busca a pessoa
    pessoa = Pessoa.query.filter_by(cpf=cpf_formatado).first()
    
    if not pessoa:
        flash('Pessoa não encontrada.', 'danger')
        return redirect(url_for('pessoas.index'))
    
    # Gera o QR code se não existir
    if not pessoa.qr_code_url:
        pessoa.qr_code_url = generate_person_qr_code(pessoa)
        db.session.commit()
    
    return render_template('qr/pessoa_qr.html', 
                           pessoa=pessoa, 
                           qr_code_url=pessoa.qr_code_url,
                           title=f'QR Code - {pessoa.nome}')

@qr_bp.route('/gerar-qrcode-ingresso/<int:id>')
@login_required
def gerar_qrcode_ingresso(id):
    """Gera ou recupera um código QR para um ingresso"""
    # Busca o ingresso
    ingresso = Ingresso.query.get_or_404(id)
    
    # Gera o QR code se não existir
    if not ingresso.qr_code_url:
        ingresso.qr_code_url = generate_entrance_qr_code(ingresso)
        db.session.commit()
    
    # Também busca a pessoa relacionada
    pessoa = Pessoa.query.filter_by(cpf=ingresso.cpf).first()
    
    return render_template('qr/ingresso_qr.html', 
                           ingresso=ingresso, 
                           pessoa=pessoa,
                           qr_code_url=ingresso.qr_code_url,
                           title=f'QR Code - Ingresso {id}')

@qr_bp.route('/quick-checkin/<cpf>')
@login_required
def quick_checkin(cpf):
    """Rota para check-in rápido de uma pessoa com QR Code"""
    # Normaliza o CPF
    cpf_normalizado = re.sub(r'[^0-9]', '', cpf)
    cpf_formatado = format_cpf(cpf_normalizado)
    
    # Busca a pessoa
    pessoa = Pessoa.query.filter_by(cpf=cpf_formatado).first()
    
    if not pessoa:
        flash('Pessoa não encontrada.', 'danger')
        return redirect(url_for('ingressos.index'))
    
    # Verifica se a pessoa já tem um ingresso aberto (sem saída registrada)
    ingresso_aberto = Ingresso.query.filter_by(cpf=pessoa.cpf, saida=None).first()
    
    if ingresso_aberto:
        flash(f'A pessoa {pessoa.nome} já possui um ingresso aberto. Registre a saída primeiro.', 'warning')
        return redirect(url_for('ingressos.visualizar', id=ingresso_aberto.id))
    
    # Prepara formulário pré-preenchido para registro rápido
    # Redireciona para formulário de novo ingresso pré-preenchido
    return render_template('qr/quick_checkin.html', 
                          pessoa=pessoa,
                          title='Check-in Rápido')

@qr_bp.route('/processar-checkin', methods=['POST'])
@login_required
def processar_checkin():
    """Processa o formulário de check-in rápido"""
    # Captura os dados do formulário
    cpf = request.form.get('cpf')
    motivo = request.form.get('motivo')
    pessoa_setor = request.form.get('pessoa_setor')
    observacoes = request.form.get('observacoes')
    
    # Verifica se os campos obrigatórios foram preenchidos
    if not cpf or not motivo or not pessoa_setor:
        flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
        return redirect(url_for('qr.quick_checkin', cpf=cpf))
    
    # Busca a pessoa
    pessoa = Pessoa.query.filter_by(cpf=cpf).first()
    
    if not pessoa:
        flash('Pessoa não encontrada.', 'danger')
        return redirect(url_for('ingressos.index'))
    
    # Obtém a data e hora atual
    current_time = get_brasil_datetime()
    
    # Formata data e hora
    data_atual = current_time.strftime('%d/%m/%Y')
    hora_atual = current_time.strftime('%H:%M')
    
    # Cria um novo ingresso
    novo_ingresso = Ingresso(
        cpf=cpf,
        data=data_atual,
        entrada=hora_atual,
        saida=None,
        motivo=motivo,
        pessoa_setor=pessoa_setor,
        observacoes=observacoes
    )
    
    # Salva no banco de dados
    db.session.add(novo_ingresso)
    db.session.commit()
    
    # Gera QR code para o novo ingresso
    novo_ingresso.qr_code_url = generate_entrance_qr_code(novo_ingresso)
    db.session.commit()
    
    flash(f'Check-in registrado com sucesso para {pessoa.nome}!', 'success')
    
    # Redireciona para visualização do QR code 
    return redirect(url_for('qr.gerar_qrcode_ingresso', id=novo_ingresso.id))

@qr_bp.route('/quick-checkout/<int:ingresso_id>')
@login_required
def quick_checkout(ingresso_id):
    """Rota para check-out rápido usando QR Code"""
    # Busca o ingresso
    ingresso = Ingresso.query.get_or_404(ingresso_id)
    
    # Verifica se o ingresso já tem saída registrada
    if ingresso.saida:
        flash('Este ingresso já possui saída registrada.', 'warning')
        return redirect(url_for('ingressos.visualizar', id=ingresso.id))
    
    # Busca a pessoa
    pessoa = Pessoa.query.filter_by(cpf=ingresso.cpf).first()
    
    return render_template('qr/confirmar_checkout.html', 
                          ingresso=ingresso,
                          pessoa=pessoa,
                          title='Confirmar Check-out')

@qr_bp.route('/processar-checkout/<int:ingresso_id>', methods=['POST'])
@login_required
def processar_checkout(ingresso_id):
    """Processa o check-out rápido"""
    # Busca o ingresso
    ingresso = Ingresso.query.get_or_404(ingresso_id)
    
    # Verifica se o ingresso já tem saída registrada
    if ingresso.saida:
        flash('Este ingresso já possui saída registrada.', 'warning')
        return redirect(url_for('ingressos.visualizar', id=ingresso.id))
    
    # Obtém a hora atual para registrar a saída
    current_time = get_brasil_datetime()
    hora_atual = current_time.strftime('%H:%M')
    
    # Atualiza a hora de saída
    ingresso.saida = hora_atual
    db.session.commit()
    
    # Busca a pessoa relacionada
    pessoa = Pessoa.query.filter_by(cpf=ingresso.cpf).first()
    
    flash(f'Check-out registrado com sucesso para {pessoa.nome if pessoa else "visitante"}!', 'success')
    return redirect(url_for('ingressos.index'))