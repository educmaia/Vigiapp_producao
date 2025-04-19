from flask import (
    Blueprint, render_template, send_file, request
)
from flask_login import login_required
from models import Pessoa, Ingresso, Empresa, Entrega, Correspondencia, Ocorrencia
from forms import RelatorioForm
from utils import generate_pdf_report, get_brasil_datetime
import os
import tempfile

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = RelatorioForm()
    
    # Pre-fill date range with current month if not submitted with Brazil timezone
    if request.method == 'GET':
        today = get_brasil_datetime()
        form.data_fim.data = today.date()
        form.data_inicio.data = today.replace(day=1).date()
    
    if form.validate_on_submit():
        tipo_relatorio = form.tipo_relatorio.data
        data_inicio = form.data_inicio.data
        data_fim = form.data_fim.data
        
        # Generate and send the report
        return gerar_relatorio(tipo_relatorio, data_inicio, data_fim)
    
    return render_template('relatorios/index.html', form=form)

def gerar_relatorio(tipo_relatorio, data_inicio, data_fim):
    # Create a temporary file to store the report
    fd, temp_path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    
    filename = f"{tipo_relatorio}_{data_inicio.strftime('%Y%m%d')}_{data_fim.strftime('%Y%m%d')}.pdf"
    
    # Format date strings for display
    data_inicio_str = data_inicio.strftime("%d/%m/%Y")
    data_fim_str = data_fim.strftime("%d/%m/%Y")
    
    if tipo_relatorio == 'ingressos':
        # Get ingressos within date range
        ingressos = Ingresso.query.join(Pessoa).filter(
            Ingresso.data.between(data_inicio_str, data_fim_str)
        ).order_by(Ingresso.data.desc(), Ingresso.entrada.desc()).all()
        
        # Prepare data for report
        data = []
        for ingresso in ingressos:
            pessoa = Pessoa.query.get(ingresso.cpf)
            data.append([
                ingresso.data, 
                ingresso.entrada, 
                ingresso.saida or "-", 
                pessoa.nome, 
                pessoa.cpf, 
                ingresso.motivo, 
                ingresso.pessoa_setor
            ])
        
        headers = ["Data", "Entrada", "Saída", "Nome", "CPF", "Motivo", "Pessoa/Setor"]
        title = "Relatório de Ingressos"
        
    elif tipo_relatorio == 'pessoas':
        # Get all pessoas
        pessoas = Pessoa.query.order_by(Pessoa.nome).all()
        
        # Prepare data for report
        data = []
        for pessoa in pessoas:
            data.append([
                pessoa.cpf,
                pessoa.nome,
                pessoa.telefone or "-",
                pessoa.empresa or "-"
            ])
        
        headers = ["CPF", "Nome", "Telefone", "Empresa"]
        title = "Relatório de Pessoas Cadastradas"
        
    elif tipo_relatorio == 'empresas':
        # Get all empresas
        empresas = Empresa.query.order_by(Empresa.nome_empresa).all()
        
        # Prepare data for report
        data = []
        for empresa in empresas:
            data.append([
                empresa.cnpj,
                empresa.nome_empresa,
                empresa.telefone_empresa or "-",
                empresa.nome_func or "-",
                empresa.telefone_func or "-"
            ])
        
        headers = ["CNPJ", "Empresa", "Telefone", "Funcionário", "Telefone Func."]
        title = "Relatório de Empresas"
        
    elif tipo_relatorio == 'entregas':
        # Get entregas within date range
        entregas = Entrega.query.join(Empresa).filter(
            Entrega.data_registro.between(data_inicio_str, data_fim_str)
        ).order_by(Entrega.data_registro.desc(), Entrega.hora_registro.desc()).all()
        
        # Prepare data for report
        data = []
        for entrega in entregas:
            empresa = Empresa.query.get(entrega.cnpj)
            status = "Pendente" if not entrega.data_envio else "Enviado"
            data.append([
                entrega.data_registro,
                entrega.hora_registro,
                empresa.nome_empresa,
                entrega.nota_fiscal or "-",
                status,
                entrega.data_envio or "-",
                entrega.hora_envio or "-"
            ])
        
        headers = ["Data", "Hora", "Empresa", "Nota Fiscal", "Status", "Data Envio", "Hora Envio"]
        title = "Relatório de Entregas"
        
    elif tipo_relatorio == 'correspondencias':
        # Convert string dates to datetime objects for comparison
        data_inicio_dt = data_inicio
        data_fim_dt = data_fim
        
        # Get correspondencias within date range
        correspondencias = Correspondencia.query.filter(
            Correspondencia.data_recebimento.between(data_inicio_dt, data_fim_dt)
        ).order_by(Correspondencia.data_recebimento.desc()).all()
        
        # Prepare data for report
        data = []
        for correspondencia in correspondencias:
            status = "Pendente" if not correspondencia.data_destinacao else "Entregue"
            data.append([
                correspondencia.data_recebimento.strftime("%d/%m/%Y"),
                correspondencia.hora_recebimento.strftime("%H:%M"),
                correspondencia.remetente,
                correspondencia.destinatario,
                correspondencia.tipo,
                correspondencia.setor_encomenda,
                status
            ])
        
        headers = ["Data", "Hora", "Remetente", "Destinatário", "Tipo", "Setor", "Status"]
        title = "Relatório de Correspondências"
        
    elif tipo_relatorio == 'ocorrencias':
        # Convert string dates to datetime objects for comparison
        data_inicio_dt = data_inicio
        data_fim_dt = data_fim
        
        # Get ocorrencias within date range
        ocorrencias = Ocorrencia.query.filter(
            Ocorrencia.data_registro.between(data_inicio_dt, data_fim_dt)
        ).order_by(Ocorrencia.data_registro.desc()).all()
        
        # Prepare data for report
        data = []
        for ocorrencia in ocorrencias:
            data.append([
                ocorrencia.data_registro.strftime("%d/%m/%Y"),
                ocorrencia.hora_registro.strftime("%H:%M"),
                ocorrencia.vigilante,
                ocorrencia.envolvidos,
                ocorrencia.gravidade.upper(),
                ocorrencia.ocorrencia[:100] + "..." if len(ocorrencia.ocorrencia) > 100 else ocorrencia.ocorrencia
            ])
        
        headers = ["Data", "Hora", "Vigilante", "Envolvidos", "Gravidade", "Descrição"]
        title = "Relatório de Ocorrências"
    
    # Generate the PDF report
    generate_pdf_report(
        data=data,
        title=title,
        headers=headers,
        filename=temp_path,
        date_range=(data_inicio_str, data_fim_str)
    )
    
    # Send the file for download
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
