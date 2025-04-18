/**
 * Script dedicado para operações de exclusão no VigiAPP
 * Corrige problemas de interação com modais e assegura
 * que os formulários de exclusão sejam enviados corretamente
 * 
 * Versão 2.0 - Implementação completa e corrigida
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando operações de exclusão VigiAPP v2.0');
    
    // Função para configurar os modais e formulários
    function setupDeleteModal(modalElement) {
        if (!modalElement) return;
        
        // Forçar o modal a ser exibido corretamente
        modalElement.classList.add('modal-force-display');
        
        // Ajustar zIndex para garantir visibilidade
        modalElement.style.zIndex = '1055';
        
        // Encontrar o formulário de exclusão
        const deleteForm = modalElement.querySelector('form.delete-form');
        if (!deleteForm) {
            console.error('Formulário de exclusão não encontrado no modal');
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
            
            // Adicionar novo listener que garantirá o envio correto
            newButton.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                
                console.log('Formulário sendo enviado:', deleteForm.action);
                
                // Submeter o formulário diretamente
                deleteForm.submit();
                
                // Esconder o modal
                const bsModal = bootstrap.Modal.getInstance(modalElement);
                if (bsModal) {
                    bsModal.hide();
                } else {
                    // Ocultação forçada se não conseguirmos obter a instância
                    modalElement.style.display = 'none';
                    const backdrop = document.querySelector('.modal-backdrop');
                    if (backdrop && backdrop.parentNode) {
                        backdrop.parentNode.removeChild(backdrop);
                    }
                    document.body.classList.remove('modal-open');
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';
                }
                
                // Recarregar a página após um pequeno atraso para permitir que o backend processe
                setTimeout(function() {
                    window.location.reload();
                }, 300);
            });
        }
    }
    
    // Função para configurar os botões de exclusão
    function setupDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.btn-delete');
        console.log(`Encontrados ${deleteButtons.length} botões de exclusão`);
        
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
                
                // Aplicar configurações ao modal antes de exibi-lo
                setupDeleteModal(modalElement);
                
                // Exibir o modal
                const modal = new bootstrap.Modal(modalElement);
                modal.show();
            });
        });
    }
    
    // Inicialização
    setupDeleteButtons();
    
    // Configurar os modais já existentes na página
    document.querySelectorAll('.modal').forEach(setupDeleteModal);
    
    // Re-inicializar após carregamento de DataTables
    document.addEventListener('draw.dt', function() {
        console.log('DataTable atualizado - reconfigurando botões de exclusão');
        setupDeleteButtons();
    });
});