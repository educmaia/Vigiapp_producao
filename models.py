from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='controlador', nullable=False)  # 'admin' or 'controlador'
    active = db.Column(db.Boolean, default=True, nullable=False)  # Status ativo/inativo
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)  # Último login
    
    def is_active(self):
        # Sobrescreve o método is_active do Flask-Login
        return self.active

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    cpf = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    empresa = db.Column(db.String(100))
    qr_code_url = db.Column(db.String(255))  # URL para o código QR desta pessoa
    ingressos = db.relationship('Ingresso', backref='pessoa', lazy=True)

class Ingresso(db.Model):
    __tablename__ = 'ingressos'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), db.ForeignKey('pessoas.cpf'), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    entrada = db.Column(db.String(10), nullable=False)
    saida = db.Column(db.String(10))
    motivo = db.Column(db.String(200), nullable=False)
    pessoa_setor = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)
    qr_code_url = db.Column(db.String(255))  # URL para o código QR deste ingresso

class Empresa(db.Model):
    __tablename__ = 'empresas'
    cnpj = db.Column(db.String(18), primary_key=True)
    nome_empresa = db.Column(db.String(100), nullable=False)
    telefone_empresa = db.Column(db.String(20))
    coringa = db.Column(db.String(100))
    nome_func = db.Column(db.String(100))
    telefone_func = db.Column(db.String(20))
    entregas = db.relationship('Entrega', backref='empresa', lazy=True, cascade='all, delete-orphan')

class EntregaImagem(db.Model):
    __tablename__ = 'entrega_imagens'
    id = db.Column(db.Integer, primary_key=True)
    entrega_id = db.Column(db.Integer, db.ForeignKey('entregas.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamento com Entrega
    entrega = db.relationship('Entrega', back_populates='imagens')

class Entrega(db.Model):
    __tablename__ = 'entregas'
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), db.ForeignKey('empresas.cnpj', ondelete='CASCADE'), nullable=False)
    data_registro = db.Column(db.String(10), nullable=False)
    hora_registro = db.Column(db.String(10), nullable=False)
    data_envio = db.Column(db.String(10))
    hora_envio = db.Column(db.String(10))
    nota_fiscal = db.Column(db.String(50))
    imagem_filename = db.Column(db.String(255))  # Campo mantido para compatibilidade
    observacoes = db.Column(db.Text)
    
    # Relacionamento com EntregaImagem
    imagens = db.relationship('EntregaImagem', back_populates='entrega', cascade='all, delete-orphan')

class Sugestao(db.Model):
    __tablename__ = 'sugestoes'
    id = db.Column(db.Integer, primary_key=True)
    sugestao = db.Column(db.Text, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.now)

class Correspondencia(db.Model):
    __tablename__ = 'correspondencias'
    id_correspondencia = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.String(100), nullable=False)
    destinatario = db.Column(db.String(100), nullable=False)
    data_recebimento = db.Column(db.Date, nullable=False)
    hora_recebimento = db.Column(db.Time, nullable=False)
    data_destinacao = db.Column(db.Date)
    hora_destinacao = db.Column(db.Time)
    tipo = db.Column(db.String(50), nullable=False)
    setor_encomenda = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)

class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'
    id_ocorrencia = db.Column(db.Integer, primary_key=True)
    vigilante = db.Column(db.String(100), nullable=False)
    envolvidos = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    hora_registro = db.Column(db.Time, nullable=False)
    gravidade = db.Column(db.String(50))
    ocorrencia = db.Column(db.Text, nullable=False)
