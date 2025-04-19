// Interações e animações específicas para QR codes no VigiAPP

document.addEventListener('DOMContentLoaded', function() {
    // Aplicar classes e estilos aos QR codes
    applyQRCodeStyling();
    
    // Adicionar eventos de interação
    setupQRInteractions();
    
    // Configurar botões de impressão
    setupPrintButtons();
    
    // Detectar e configurar QR codes de checkout
    setupCheckoutQRs();
});

// Aplica estilos aos QR codes
function applyQRCodeStyling() {
    // Encontrar todas as imagens de QR code
    const qrImages = document.querySelectorAll('img[src*="qrcodes/"]');
    
    qrImages.forEach(img => {
        // Adicionar classe para estilização
        img.classList.add('qr-code-image');
        
        // Envolver imagem em container estilizado, se ainda não estiver
        if (!img.closest('.qr-container')) {
            const parent = img.parentNode;
            
            // Criar container
            const container = document.createElement('div');
            container.className = 'qr-container';
            
            // Determinar o tipo de QR baseado no src
            const qrType = img.src.includes('pessoa_') ? 'check-in' : 'check-out';
            
            // Adicionar badge
            const badge = document.createElement('div');
            badge.className = 'qr-badge';
            badge.textContent = qrType === 'check-in' ? 'Check-in' : 'Check-out';
            container.appendChild(badge);
            
            // Mover a imagem para o container
            parent.replaceChild(container, img);
            container.appendChild(img);
            
            // Adicionar informações e botão de impressão
            addQRInfo(container, qrType);
        }
    });
}

// Adiciona informações e instruções ao container QR
function addQRInfo(container, type) {
    // Criar seção de info
    const infoDiv = document.createElement('div');
    infoDiv.className = 'qr-info';
    
    // Adicionar instruções baseadas no tipo
    const instrDiv = document.createElement('div');
    instrDiv.className = 'qr-instructions';
    
    if (type === 'check-in') {
        instrDiv.innerHTML = `
            <div><i class="fas fa-info-circle qr-icon"></i> <strong>Instruções:</strong></div>
            <p>Utilize este QR code para registrar rapidamente a entrada do visitante sem precisar digitar o CPF.</p>
            <ol>
                <li>Apresente este QR code ao responsável pela portaria.</li>
                <li>Após a leitura, confirme os detalhes da visita.</li>
                <li>Pronto! O registro de entrada será feito automaticamente.</li>
            </ol>
        `;
    } else {
        instrDiv.innerHTML = `
            <div><i class="fas fa-info-circle qr-icon"></i> <strong>Instruções:</strong></div>
            <p>Utilize este QR code para registrar rapidamente a saída do visitante.</p>
            <ol>
                <li>Apresente este QR code ao responsável pela portaria antes de sair.</li>
                <li>Após a leitura, a saída será registrada automaticamente.</li>
                <li>Guarde este código até o final da sua visita.</li>
            </ol>
        `;
    }
    
    infoDiv.appendChild(instrDiv);
    
    // Adicionar botão de impressão
    const printBtn = document.createElement('button');
    printBtn.className = 'btn btn-sm btn-light print-button';
    printBtn.innerHTML = '<i class="fas fa-print"></i> Imprimir QR Code';
    printBtn.onclick = function() {
        window.print();
    };
    
    infoDiv.appendChild(printBtn);
    container.appendChild(infoDiv);
}

// Configura interações para os QR codes
function setupQRInteractions() {
    const containers = document.querySelectorAll('.qr-container');
    
    containers.forEach(container => {
        // Adicionar efeito de hover/focus para acessibilidade
        container.setAttribute('tabindex', '0');
        
        // Efeito de clique para copiar URL (se aplicável)
        container.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img && img.src) {
                // Adicionar efeito visual de clique
                this.classList.add('clicked');
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 200);
                
                // Efeito de pulsação
                animateQRContainer(this);
            }
        });
    });
}

// Anima container do QR code
function animateQRContainer(container) {
    container.classList.add('success-animation');
    setTimeout(() => {
        container.classList.remove('success-animation');
    }, 1000);
}

// Configura botões de impressão
function setupPrintButtons() {
    document.querySelectorAll('.print-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Adicionar classe temporária para estilo de impressão
            document.body.classList.add('printing-qr');
            
            // Imprimir
            window.print();
            
            // Remover classe após imprimir
            setTimeout(() => {
                document.body.classList.remove('printing-qr');
            }, 1000);
        });
    });
    
    // Adicionar estilos para impressão
    if (!document.getElementById('print-styles')) {
        const printStyle = document.createElement('style');
        printStyle.id = 'print-styles';
        printStyle.textContent = `
            @media print {
                body * {
                    visibility: hidden;
                }
                .printing-qr .qr-container, .printing-qr .qr-container * {
                    visibility: visible;
                }
                .printing-qr .qr-container {
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    box-shadow: none !important;
                }
                .printing-qr .qr-container .print-button {
                    display: none !important;
                }
            }
        `;
        document.head.appendChild(printStyle);
    }
}

// Configura QR codes específicos para checkout
function setupCheckoutQRs() {
    // Verificar se estamos na página de confirmar checkout
    if (window.location.href.includes('quick-checkout') || 
        window.location.href.includes('confirmar-checkout')) {
        
        const qrContainers = document.querySelectorAll('.qr-container');
        qrContainers.forEach(container => {
            container.classList.add('checkout-qr');
        });
        
        // Adicionar efeito pulsante ao botão de confirmação
        const confirmBtn = document.querySelector('button[type="submit"]');
        if (confirmBtn) {
            confirmBtn.classList.add('pulse-button');
        }
    }
}

// Função para mostrar animação ao escanear QR code
function showScanAnimation() {
    const scanOverlay = document.createElement('div');
    scanOverlay.className = 'scan-overlay';
    scanOverlay.innerHTML = `
        <div class="scan-animation">
            <div class="scan-line"></div>
        </div>
        <div class="scan-text">Escaneando...</div>
    `;
    
    document.body.appendChild(scanOverlay);
    
    setTimeout(() => {
        scanOverlay.classList.add('scan-complete');
        scanOverlay.querySelector('.scan-text').textContent = 'QR Code reconhecido!';
        
        setTimeout(() => {
            scanOverlay.remove();
        }, 1000);
    }, 1500);
}