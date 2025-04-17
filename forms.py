from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField, SelectField,
    DateField, TimeField, HiddenField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError, Optional
)
import re
from datetime import datetime

def validate_cpf(form, field):
    # Remove non-numeric characters for validation
    cpf = re.sub(r'[^0-9]', '', field.data)
    
    # Check if CPF has 11 digits
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 dígitos numéricos.')
    
    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido.')
    
    # Calculate first verification digit
    sum_of_products = 0
    for i in range(9):
        sum_of_products += int(cpf[i]) * (10 - i)
    verification_digit = (sum_of_products * 10) % 11
    if verification_digit == 10:
        verification_digit = 0
    if verification_digit != int(cpf[9]):
        raise ValidationError('CPF inválido.')
    
    # Calculate second verification digit
    sum_of_products = 0
    for i in range(10):
        sum_of_products += int(cpf[i]) * (11 - i)
    verification_digit = (sum_of_products * 10) % 11
    if verification_digit == 10:
        verification_digit = 0
    if verification_digit != int(cpf[10]):
        raise ValidationError('CPF inválido.')

def validate_cnpj(form, field):
    # Remove non-numeric characters for validation
    cnpj = re.sub(r'[^0-9]', '', field.data)
    
    # Check if CNPJ has 14 digits
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve conter 14 dígitos numéricos.')
    
    # Check if all digits are the same (invalid CNPJ)
    if cnpj == cnpj[0] * 14:
        raise ValidationError('CNPJ inválido.')
    
    # Calculate first verification digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_of_products = 0
    for i in range(12):
        sum_of_products += int(cnpj[i]) * weights[i]
    verification_digit = sum_of_products % 11
    if verification_digit < 2:
        verification_digit = 0
    else:
        verification_digit = 11 - verification_digit
    if verification_digit != int(cnpj[12]):
        raise ValidationError('CNPJ inválido.')
    
    # Calculate second verification digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_of_products = 0
    for i in range(13):
        sum_of_products += int(cnpj[i]) * weights[i]
    verification_digit = sum_of_products % 11
    if verification_digit < 2:
        verification_digit = 0
    else:
        verification_digit = 11 - verification_digit
    if verification_digit != int(cnpj[13]):
        raise ValidationError('CNPJ inválido.')

def validate_telefone(form, field):
    # Check if phone number matches the expected format
    telefone = field.data
    if telefone and not re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', telefone):
        raise ValidationError('Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Função', choices=[('vigilante', 'Vigilante'), ('admin', 'Administrador')])
    submit = SubmitField('Registrar')

class PessoaForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), validate_cpf])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    telefone = StringField('Telefone', validators=[Optional(), validate_telefone])
    empresa = StringField('Empresa', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Salvar')

class IngressoForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), validate_cpf])
    data = StringField('Data', validators=[DataRequired()])
    entrada = StringField('Entrada', validators=[DataRequired()])
    saida = StringField('Saída', validators=[Optional()])
    motivo = StringField('Motivo', validators=[DataRequired(), Length(max=200)])
    pessoa_setor = StringField('Pessoa/Setor', validators=[DataRequired(), Length(max=100)])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Registrar')

class EmpresaForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), validate_cnpj])
    nome_empresa = StringField('Nome da Empresa', validators=[DataRequired(), Length(max=100)])
    telefone_empresa = StringField('Telefone da Empresa', validators=[Optional(), validate_telefone])
    coringa = StringField('Coringa', validators=[Optional(), Length(max=100)])
    nome_func = StringField('Nome do Funcionário', validators=[Optional(), Length(max=100)])
    telefone_func = StringField('Telefone do Funcionário', validators=[Optional(), validate_telefone])
    submit = SubmitField('Salvar')

class EntregaForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), validate_cnpj])
    data_registro = StringField('Data de Registro', validators=[DataRequired()])
    hora_registro = StringField('Hora de Registro', validators=[DataRequired()])
    data_envio = StringField('Data de Envio', validators=[Optional()])
    hora_envio = StringField('Hora de Envio', validators=[Optional()])
    nota_fiscal = StringField('Nota Fiscal', validators=[Optional(), Length(max=50)])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Registrar')

class CorrespondenciaForm(FlaskForm):
    remetente = StringField('Remetente', validators=[DataRequired(), Length(max=100)])
    destinatario = StringField('Destinatário', validators=[DataRequired(), Length(max=100)])
    data_recebimento = DateField('Data de Recebimento', validators=[DataRequired()], format='%Y-%m-%d')
    hora_recebimento = TimeField('Hora de Recebimento', validators=[DataRequired()], format='%H:%M')
    data_destinacao = DateField('Data de Destinação', validators=[Optional()], format='%Y-%m-%d')
    hora_destinacao = TimeField('Hora de Destinação', validators=[Optional()], format='%H:%M')
    tipo = SelectField('Tipo', choices=[
        ('carta', 'Carta'), 
        ('pacote', 'Pacote'), 
        ('encomenda', 'Encomenda'),
        ('documento', 'Documento'),
        ('outros', 'Outros')
    ], validators=[DataRequired()])
    setor_encomenda = StringField('Setor/Encomenda', validators=[DataRequired(), Length(max=100)])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Registrar')

class OcorrenciaForm(FlaskForm):
    vigilante = StringField('Vigilante', validators=[DataRequired(), Length(max=100)])
    envolvidos = StringField('Envolvidos', validators=[DataRequired(), Length(max=200)])
    data_registro = DateField('Data de Registro', validators=[DataRequired()], format='%Y-%m-%d')
    hora_registro = TimeField('Hora de Registro', validators=[DataRequired()], format='%H:%M')
    gravidade = SelectField('Gravidade', choices=[
        ('baixa', 'Baixa'), 
        ('media', 'Média'), 
        ('alta', 'Alta'),
        ('critica', 'Crítica')
    ], validators=[DataRequired()])
    ocorrencia = TextAreaField('Ocorrência', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class RelatorioForm(FlaskForm):
    tipo_relatorio = SelectField('Tipo de Relatório', choices=[
        ('ingressos', 'Ingressos'),
        ('pessoas', 'Pessoas'),
        ('empresas', 'Empresas'),
        ('entregas', 'Entregas'),
        ('correspondencias', 'Correspondências'),
        ('ocorrencias', 'Ocorrências')
    ], validators=[DataRequired()])
    data_inicio = DateField('Data Início', validators=[DataRequired()], format='%Y-%m-%d')
    data_fim = DateField('Data Fim', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Gerar Relatório')
