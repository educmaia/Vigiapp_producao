// Animações e Micro-interações para o VigiAPP

document.addEventListener('DOMContentLoaded', function() {
    // Adiciona classe de animação a todos os cartões ao carregar
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100); // Atraso escalonado para efeito de cascata
    });

    // Adiciona classe para linhas de tabela
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.classList.add('table-row-highlight');
    });

    // Adiciona classe de pulsação para botões importantes
    const actionButtons = document.querySelectorAll('.btn-success, .btn-primary');
    actionButtons.forEach(button => {
        button.classList.add('pulse-button');
    });

    // Adiciona classe de animação para QR codes
    const qrCodes = document.querySelectorAll('.qr-code-image');
    qrCodes.forEach(qr => {
        qr.classList.add('qr-highlight');
    });

    // Animação para alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.add('alert-fade');
        
        // Auto-fechar alertas após 5 segundos
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                // Cria uma animação de desaparecimento
                alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                
                // Remove o alerta do DOM após a animação
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }, 5000);
        }
    });

    // Adiciona efeito de transição para links de navegação
    const navLinks = document.querySelectorAll('nav a, .breadcrumb a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Não aplica a animações para links que abrem em nova janela ou têm comportamento especial
            if (this.target === '_blank' || this.dataset.toggle || this.dataset.bs) {
                return;
            }
            
            e.preventDefault();
            const href = this.getAttribute('href');
            
            // Aplica efeito de fade-out à página atual
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.3s ease';
            
            // Navega para o novo URL após a animação
            setTimeout(() => {
                window.location.href = href;
            }, 300);
        });
    });

    // Adiciona efeito de loading para formulários
    const forms = document.querySelectorAll('form:not([data-no-loading])');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Encontra o botão de submit
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                // Salva o texto original
                const originalText = submitButton.innerHTML;
                
                // Adiciona spinner e desabilita o botão
                submitButton.innerHTML = '<span class="loading-spinner"></span> Processando...';
                submitButton.disabled = true;
                
                // Restaura o botão se o envio levar mais de 10 segundos (caso de timeout)
                setTimeout(() => {
                    if (submitButton.disabled) {
                        submitButton.innerHTML = originalText;
                        submitButton.disabled = false;
                    }
                }, 10000);
            }
        });
    });

    // Efeito para inputs de formulário
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.classList.add('focus-border');
        
        // Adiciona efeito de destaque ao focar
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.classList.remove('input-focused');
        });
    });

    // Animação de sucesso para operações bem-sucedidas
    if (document.querySelector('.alert-success')) {
        const successCards = document.querySelectorAll('.card');
        successCards.forEach(card => {
            card.classList.add('success-animation');
        });
    }

    // Efeito hover para botões de ação
    const hoverButtons = document.querySelectorAll('.btn-info, .btn-warning, .btn-danger');
    hoverButtons.forEach(button => {
        button.classList.add('action-button');
    });

    // Adiciona animação de página para o conteúdo principal
    const mainContent = document.querySelector('main') || document.querySelector('.container');
    if (mainContent) {
        mainContent.classList.add('page-transition');
    }
});

// Funções utilitárias para animações

// Mostra notificação animada
function showAnimatedNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `animated-notification ${type} alert-fade`;
    notification.innerHTML = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adiciona efeito de pulsação a um elemento
function pulseElement(element) {
    element.classList.add('notification-badge');
    setTimeout(() => {
        element.classList.remove('notification-badge');
    }, 2000);
}

// Aplica animação de sucesso a um elemento
function animateSuccess(element) {
    element.classList.add('success-animation');
    setTimeout(() => {
        element.classList.remove('success-animation');
    }, 1000);
}