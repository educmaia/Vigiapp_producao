/**
 * Script dedicado para operações de exclusão no VigiAPP
 * Versão 4.0 - Suporte a páginas de confirmação dedicadas
 * 
 * Foram removidos os recursos legados de confirmação por modal.
 * Todas as confirmações agora são redirecionadas para páginas dedicadas.
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando operações de exclusão VigiAPP v4.0');
    
    // Verificar se estamos na página de empresas e remover qualquer modal de exclusão antigo
    if (window.location.pathname.includes('/empresas')) {
        // Remover modais de exclusão antigos que possam ter sido adicionados incorretamente
        document.querySelectorAll('.modal[id^="deleteModal"]').forEach(function(modal) {
            if (modal && modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        });
        
        // Garantir que nenhum backdrop de modal esteja presente
        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
            if (backdrop && backdrop.parentNode) {
                backdrop.parentNode.removeChild(backdrop);
            }
        });
        
        // Remover classes do body que possam ter sido adicionadas
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        
        console.log('Página de empresas: limpeza de modais concluída');
    }
    
    // Função para configurar os formulários nas novas páginas de confirmação
    function setupConfirmationPages() {
        // Nas páginas de confirmação dedicadas temos um formulário simples
        const confirmForm = document.querySelector('.card-body form');
        if (confirmForm) {
            console.log('Formulário de confirmação encontrado na página dedicada');
        }
    }
    
    // Função para configurar os botões de exclusão do tipo modal apenas para outras seções (legado)
    function setupLegacyDeleteButtons() {
        // Não executa esta função na página de empresas
        if (window.location.pathname.includes('/empresas')) {
            return;
        }
        
        const deleteButtons = document.querySelectorAll('.btn-delete[data-bs-target^="#deleteModal"]');
        console.log(`Encontrados ${deleteButtons.length} botões de exclusão (modais)`);
        
        if (deleteButtons.length === 0) {
            return;
        }
        
        deleteButtons.forEach(function(button) {
            // Esta parte só é executada para outras seções que ainda usam o sistema antigo
            // Pode ser removida no futuro quando todas as seções forem migradas
        });
    }
    
    // Inicialização
    setupConfirmationPages();
    setupLegacyDeleteButtons();
});