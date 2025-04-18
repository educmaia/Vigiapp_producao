/**
 * Script dedicado para operações de exclusão no VigiAPP
 * Versão 3.0 - Suporte a páginas de confirmação dedicadas
 * 
 * Agora suporta dois fluxos:
 * 1. Modais de confirmação (legado)
 * 2. Páginas dedicadas de confirmação (nova abordagem)
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando operações de exclusão VigiAPP v3.0');
    
    // Função para configurar os modais e formulários (legado)
    function setupDeleteModal(modalElement) {
        if (!modalElement) return;
        
        // Forçar o modal a ser exibido corretamente
        modalElement.classList.add('modal-force-display');
        modalElement.style.zIndex = '1055';
        
        // Encontrar o formulário de exclusão
        const deleteForm = modalElement.querySelector('form.delete-form');
        if (!deleteForm) {
            // Isso é esperado nas páginas que usam a nova abordagem
            return;
        }
        
        // Garantir que o botão tenha a classe correta
        const confirmButton = modalElement.querySelector('.btn-danger[type="submit"]');
        if (confirmButton && !confirmButton.classList.contains('btn-confirm-delete')) {
            confirmButton.classList.add('btn-confirm-delete');
        }
        
        // Configurar o botão de confirmação
        const submitButton = modalElement.querySelector('.btn-confirm-delete');
        if (submitButton) {
            // Remover listeners existentes para evitar duplicações
            const newButton = submitButton.cloneNode(true);
            if (submitButton.parentNode) {
                submitButton.parentNode.replaceChild(newButton, submitButton);
            }
            
            // Adicionar novo listener
            newButton.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                
                console.log('Formulário sendo enviado:', deleteForm.action);
                deleteForm.submit();
                
                // Esconder o modal
                const bsModal = bootstrap.Modal.getInstance(modalElement);
                if (bsModal) {
                    bsModal.hide();
                } else {
                    // Ocultação forçada se necessário
                    modalElement.style.display = 'none';
                    const backdrop = document.querySelector('.modal-backdrop');
                    if (backdrop && backdrop.parentNode) {
                        backdrop.parentNode.removeChild(backdrop);
                    }
                    document.body.classList.remove('modal-open');
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';
                }
                
                // Recarregar a página após um pequeno atraso
                setTimeout(function() {
                    window.location.reload();
                }, 300);
            });
        }
    }
    
    // Função para configurar os formulários nas novas páginas de confirmação
    function setupConfirmationPages() {
        // Nas páginas de confirmação dedicadas temos um formulário simples
        const confirmForm = document.querySelector('.card-body form');
        if (confirmForm) {
            console.log('Formulário de confirmação encontrado na página dedicada');
            
            // Não precisamos fazer nada especial, o formulário já funciona corretamente
            // Este código está aqui apenas para expansões futuras
        }
    }
    
    // Função para configurar os botões de exclusão do tipo modal (legado)
    function setupDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.btn-delete');
        console.log(`Encontrados ${deleteButtons.length} botões de exclusão (modais)`);
        
        if (deleteButtons.length === 0) {
            // Provavelmente estamos usando a nova abordagem
            return;
        }
        
        deleteButtons.forEach(function(button) {
            // Remove listeners existentes
            const newButton = button.cloneNode(true);
            if (button.parentNode) {
                button.parentNode.replaceChild(newButton, button);
            }
            
            // Adiciona novo listener
            newButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Obtém o ID do modal
                const modalId = this.getAttribute('data-bs-target');
                const modalElement = document.querySelector(modalId);
                
                if (!modalElement) {
                    console.error('Modal não encontrado:', modalId);
                    return;
                }
                
                // Aplicar configurações ao modal
                setupDeleteModal(modalElement);
                
                // Exibir o modal
                const modal = new bootstrap.Modal(modalElement);
                modal.show();
            });
        });
    }
    
    // Inicialização
    setupDeleteButtons();
    setupConfirmationPages();
    
    // Configurar os modais que ainda existem na página (legado)
    document.querySelectorAll('.modal').forEach(setupDeleteModal);
    
    // Re-inicializar após carregamento de DataTables
    document.addEventListener('draw.dt', function() {
        console.log('DataTable atualizado - reconfigurando botões');
        setupDeleteButtons();
    });
});