// Animações e micro-interações para o VigiAPP
// Este arquivo contém animações gerais para a aplicação que foram desativadas a pedido do usuário

document.addEventListener('DOMContentLoaded', function() {
    // Todas as animações foram desativadas conforme solicitado
    // Inicializar tooltips do Bootstrap apenas para funcionalidade (sem animações)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Nenhuma animação será inicializada
});

// Inicializa animações para cards da interface
function initializeCardAnimations() {
    // Encontrar todos os cards da aplicação
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        // Adicionar atraso escalonado aos cards para efeito de cascata
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Adicionar classe para animar entrada
        card.classList.add('fade-in-up');
        
        // Adicionar efeito de destaque ao passar o mouse
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-highlight');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-highlight');
        });
    });
}

// Configura efeitos visuais para botões
function setupButtonEffects() {
    // Adicionar efeito de onda (ripple) aos botões
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Criar elemento para efeito de onda
            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            
            // Posicionar o efeito no ponto clicado
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
            ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
            
            // Adicionar o efeito ao botão
            this.appendChild(ripple);
            
            // Remover após a animação
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Configura transições suaves entre páginas
function setupPageTransitions() {
    // Navegação direta sem efeito de congelamento
    document.querySelectorAll('a:not([target="_blank"]):not([href^="#"])').forEach(link => {
        // Não adiciona eventos especiais - a navegação ocorre de forma natural
        // Removido o efeito de congelamento conforme solicitado pelo usuário
    });
    
    // Garante que não haja classe de carregamento quando a página estiver pronta
    window.addEventListener('load', function() {
        document.body.classList.remove('page-loading');
    });
}

// Inicializa animações para tabelas
function initializeTableAnimations() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Adicionar classe para fade-in das tabelas
        table.classList.add('table-animated');
        
        // Animar linhas da tabela em cascata
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.animationDelay = `${0.05 + (index * 0.05)}s`;
            row.classList.add('table-row-animated');
        });
    });
}

// Inicializa animações para formulários
function initializeFormAnimations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Animar campos de formulário em sequência
        const fields = form.querySelectorAll('.form-group, .mb-3');
        fields.forEach((field, index) => {
            field.style.animationDelay = `${0.1 + (index * 0.05)}s`;
            field.classList.add('form-field-animated');
        });
        
        // Adicionar feedback visual ao clicar em campos
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.closest('.form-group, .mb-3')?.classList.add('focused-field');
            });
            
            input.addEventListener('blur', function() {
                this.closest('.form-group, .mb-3')?.classList.remove('focused-field');
            });
        });
    });
}

// Configura animações para mensagens flash
function setupFlashMessageAnimations() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Adicionar classe para animar entrada
        alert.classList.add('alert-animated');
        
        // Adicionar timeout para remover o alerta após alguns segundos
        setTimeout(() => {
            alert.classList.add('alert-dismissing');
            
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}