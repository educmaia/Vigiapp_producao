import os
import qrcode

# Pasta para armazenar os códigos QR gerados
QR_FOLDER = os.path.join('static', 'qrcodes')
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

def generate_qr_code(data, filename, size=10):
    """
    Gera um código QR para os dados fornecidos e salva como imagem.
    
    Args:
        data (str): Texto/URL a ser codificado no QR
        filename (str): Nome do arquivo para salvar o código QR (sem a extensão)
        size (int): Tamanho do QR (valor maior = imagem maior)
        
    Returns:
        str: Caminho do arquivo gerado
    """
    # Gera o código QR com a biblioteca
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Cria a imagem do QR Code (preto e branco)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Define o caminho completo com extensão .png
    filepath = os.path.join(QR_FOLDER, f"{filename}.png")
    
    # Salva a imagem
    img.save(filepath)
    
    return filepath

def generate_person_qr_code(pessoa):
    """
    Gera um código QR para uma pessoa específica, usando seu CPF como identificador.
    
    Args:
        pessoa: Objeto Pessoa do modelo
        
    Returns:
        str: URL para o código QR gerado
    """
    # Normaliza o CPF para usar como parte do nome do arquivo
    cpf_normalizado = pessoa.cpf.replace('.', '').replace('-', '')
    
    # Cria um QR code com uma URL para a rota de check-in/check-out rápido
    qr_data = f"/quick-checkin/{cpf_normalizado}"
    
    # Gera o nome do arquivo baseado no CPF e nome
    filename = f"pessoa_{cpf_normalizado}"
    
    # Gera o código QR
    filepath = generate_qr_code(qr_data, filename)
    
    # Retorna a URL estática para o código gerado
    return os.path.join('qrcodes', f"{filename}.png")

def generate_entrance_qr_code(ingresso):
    """
    Gera um código QR para um ingresso específico.
    
    Args:
        ingresso: Objeto Ingresso do modelo
        
    Returns:
        str: URL para o código QR gerado
    """
    # Normaliza o CPF para usar como parte do nome do arquivo
    cpf_normalizado = ingresso.cpf.replace('.', '').replace('-', '')
    
    # Cria um QR code com uma URL para a rota de registro de saída
    qr_data = f"/quick-checkout/{ingresso.id}"
    
    # Gera o nome do arquivo baseado no ID do ingresso
    filename = f"ingresso_{ingresso.id}_{cpf_normalizado}"
    
    # Gera o código QR
    filepath = generate_qr_code(qr_data, filename)
    
    # Retorna a URL estática para o código gerado
    return os.path.join('qrcodes', f"{filename}.png")