/**
 * JavaScript para otimizações móveis do VigiAPP
 * Melhora a experiência do usuário em dispositivos móveis
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detecta se é um dispositivo móvel
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Adiciona classe para identificar dispositivos móveis
        document.body.classList.add('mobile-device');
        
        // Ajusta tamanho de tabelas
        optimizeTablesForMobile();
        
        // Melhora navigação em dispositivos touch
        enhanceTouchNavigation();
        
        // Otimiza formulários para entrada em dispositivos touch
        optimizeFormsForMobile();
        
        // Adiciona suporte a upload de imagem via câmera em formulários
        enhanceMobileImageCapture();
        
        // Melhora o comportamento de modais em dispositivos móveis
        optimizeModalsForMobile();
    }
    
    // Otimiza tabelas para melhor visualização em dispositivos móveis
    function optimizeTablesForMobile() {
        // Encontra todas as tabelas que usam DataTables
        const tables = document.querySelectorAll('.dataTable');
        
        tables.forEach(table => {
            // Adiciona classe para melhorar rolagem horizontal
            const tableWrapper = table.closest('.dataTables_wrapper');
            if (tableWrapper) {
                tableWrapper.classList.add('mobile-table-wrapper');
            }
            
            // Ajusta configurações do DataTables para móvel
            if ($.fn.dataTable && $.fn.dataTable.isDataTable(table)) {
                const dataTable = $(table).DataTable();
                
                // Diminui número de itens por página para melhorar desempenho
                dataTable.page.len(5).draw();
            }
        });
        
        // Ajusta botões de ação em tabelas
        const actionButtons = document.querySelectorAll('.table .btn');
        actionButtons.forEach(btn => {
            btn.classList.add('action-btn');
        });
    }
    
    // Melhora navegação em telas de toque
    function enhanceTouchNavigation() {
        // Aumenta área de clique para links no menu principal
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        navLinks.forEach(link => {
            link.classList.add('nav-link-touch');
        });
        
        // Melhora feedback tátil ao tocar em botões e links
        document.querySelectorAll('.btn, .nav-link, .dropdown-item').forEach(el => {
            el.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });
            
            el.addEventListener('touchend', function() {
                this.classList.remove('touch-active');
            });
        });
        
        // Adiciona navegação de volta para facilitar em dispositivos móveis
        const contentDiv = document.querySelector('.container.mt-4');
        if (contentDiv && !document.querySelector('.btn-back-home') && window.location.pathname !== '/' && window.location.pathname !== '/login') {
            const backLink = document.createElement('a');
            backLink.href = '/';
            backLink.classList.add('btn', 'btn-back-home', 'mb-3', 'd-flex', 'align-items-center');
            backLink.innerHTML = '<i class="fas fa-arrow-left me-2"></i> Voltar';
            backLink.style.width = 'fit-content';
            
            contentDiv.prepend(backLink);
        }
    }
    
    // Otimiza formulários para entrada em dispositivos touch
    function optimizeFormsForMobile() {
        // Ajusta tamanhos dos inputs para facilitar digitação
        document.querySelectorAll('input, select, textarea').forEach(input => {
            input.classList.add('mobile-form-control');
        });
        
        // Para campos CPF/CNPJ, adiciona classe específica
        document.querySelectorAll('input[name="cpf"], input[name="cnpj"]').forEach(input => {
            input.classList.add('mobile-numeric-input');
        });
        
        // Ajusta o datepicker para dispositivos móveis
        document.querySelectorAll('input[type="date"], input[type="time"]').forEach(input => {
            input.style.minHeight = '44px';
        });
        
        // Agrupa botões de formulário para melhor visualização
        const formButtons = document.querySelectorAll('form .btn[type="submit"]');
        formButtons.forEach(btn => {
            btn.parentElement.classList.add('form-buttons-container');
            btn.classList.add('btn-lg');
        });
    }
    
    // Adiciona suporte a captura de imagem em dispositivos móveis
    function enhanceMobileImageCapture() {
        // Verifica se o dispositivo tem câmera
        const hasCamera = navigator.mediaDevices && navigator.mediaDevices.getUserMedia;
        
        // Busca por campos de upload de imagem
        const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        
        if (hasCamera && fileInputs.length > 0) {
            fileInputs.forEach(input => {
                // Adiciona botão para capturar imagem da câmera
                const captureBtn = document.createElement('button');
                captureBtn.type = 'button';
                captureBtn.className = 'btn btn-outline-secondary mt-2';
                captureBtn.innerHTML = '<i class="fas fa-camera me-2"></i> Usar Câmera';
                
                input.parentNode.insertBefore(captureBtn, input.nextSibling);
                
                // Adiciona evento para capturar imagem
                captureBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    // Usa input[capture] nativo do dispositivo
                    input.setAttribute('capture', 'environment');
                    input.click();
                });
                
                // Adiciona preview da imagem selecionada
                input.addEventListener('change', function() {
                    const previewDiv = this.parentNode.querySelector('.mobile-upload-preview') || document.createElement('div');
                    
                    if (!this.parentNode.querySelector('.mobile-upload-preview')) {
                        previewDiv.className = 'mobile-upload-preview mt-2';
                        this.parentNode.appendChild(previewDiv);
                    }
                    
                    if (this.files && this.files[0]) {
                        const reader = new FileReader();
                        
                        reader.onload = function(e) {
                            previewDiv.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                        }
                        
                        reader.readAsDataURL(this.files[0]);
                    } else {
                        previewDiv.innerHTML = '';
                    }
                });
            });
        }
    }
    
    // Melhora o comportamento de modais em dispositivos móveis
    function optimizeModalsForMobile() {
        // Ajusta tamanho do modal para ocupar mais espaço na tela
        document.querySelectorAll('.modal-dialog').forEach(dialog => {
            dialog.classList.add('modal-dialog-mobile');
        });
        
        // Ajusta scroll em modais para melhor experiência em touch
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const modalBody = this.querySelector('.modal-body');
                if (modalBody) {
                    modalBody.classList.add('mobile-modal-body');
                    
                    // Força o corpo a ter scroll touch suave
                    modalBody.style.webkitOverflowScrolling = 'touch';
                }
            });
        });
    }
});