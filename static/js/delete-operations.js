/**
 * Script dedicado para operações de exclusão no VigiAPP
 * Corrige problemas de interação com modais e assegura
 * que os formulários de exclusão sejam enviados corretamente
 */

document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os botões de exclusão
    const deleteButtons = document.querySelectorAll('.btn-delete');
    
    // Para cada botão de exclusão
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            // Previne comportamento padrão
            e.preventDefault();
            e.stopPropagation();
            
            // Obtém o ID do modal do data-attribute
            const modalId = this.getAttribute('data-bs-target');
            
            // Verifica se o modal existe
            const modalElement = document.querySelector(modalId);
            if (!modalElement) {
                console.error('Modal não encontrado:', modalId);
                return;
            }
            
            // Cria uma instância do modal usando Bootstrap 5
            const modalInstance = new bootstrap.Modal(modalElement);
            
            // Abre o modal
            modalInstance.show();
            
            // Encontra o formulário dentro do modal
            const deleteForm = modalElement.querySelector('form');
            if (!deleteForm) {
                console.error('Formulário de exclusão não encontrado no modal:', modalId);
                return;
            }
            
            // Adiciona evento ao botão de confirmação
            const confirmButton = modalElement.querySelector('.btn-confirm-delete');
            if (confirmButton) {
                // Remove quaisquer listeners anteriores para evitar duplicidade
                const newConfirmButton = confirmButton.cloneNode(true);
                confirmButton.parentNode.replaceChild(newConfirmButton, confirmButton);
                
                // Adiciona o novo listener
                newConfirmButton.addEventListener('click', function(event) {
                    // Previne comportamento padrão do botão
                    event.preventDefault();
                    event.stopPropagation();
                    
                    console.log('Submetendo formulário de exclusão:', deleteForm.action);
                    
                    // Submete o formulário usando fetch para debugging
                    fetch(deleteForm.action, {
                        method: 'POST',
                        body: new FormData(deleteForm),
                        credentials: 'same-origin',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(response => {
                        console.log('Resposta recebida:', response);
                        // Redireciona para a página atual após sucesso
                        window.location.reload();
                    })
                    .catch(error => {
                        console.error('Erro ao excluir item:', error);
                        alert('Erro ao excluir item: ' + error.message);
                        // Fechamos o modal de qualquer forma
                        modalInstance.hide();
                    });
                    
                    // Fecha o modal após submeter
                    modalInstance.hide();
                });
            }
        });
    });
    
    // Monitora eventos de DataTables para replicar a funcionalidade em tabelas paginadas
    document.addEventListener('draw.dt', function() {
        // Re-seleciona os botões após redraw do DataTable
        const newDeleteButtons = document.querySelectorAll('.btn-delete');
        
        newDeleteButtons.forEach(function(button) {
            // Remove qualquer listener pré-existente
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            
            // Adiciona o novo listener
            newButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const modalId = this.getAttribute('data-bs-target');
                const modalElement = document.querySelector(modalId);
                
                if (modalElement) {
                    const modalInstance = new bootstrap.Modal(modalElement);
                    modalInstance.show();
                }
            });
        });
    });
});