/**
 * Configuração do DataTables para o VigiAPP
 * Inicializa tabelas com configurações responsivas e tradução para português
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detecta se estamos em um dispositivo móvel
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // Configurações padrão para DataTables
    const defaultConfig = {
        language: {
            "sEmptyTable": "Nenhum registro encontrado",
            "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
            "sInfoFiltered": "(Filtrados de _MAX_ registros)",
            "sInfoPostFix": "",
            "sInfoThousands": ".",
            "sLengthMenu": "_MENU_ resultados por página",
            "sLoadingRecords": "Carregando...",
            "sProcessing": "Processando...",
            "sZeroRecords": "Nenhum registro encontrado",
            "sSearch": "Pesquisar:",
            "oPaginate": {
                "sNext": "Próximo",
                "sPrevious": "Anterior",
                "sFirst": "Primeiro",
                "sLast": "Último"
            },
            "oAria": {
                "sSortAscending": ": Ordenar colunas de forma ascendente",
                "sSortDescending": ": Ordenar colunas de forma descendente"
            }
        },
        // Adiciona configurações responsivas
        responsive: true,
        // Ajusta número de itens por página para dispositivos móveis
        pageLength: isMobile ? 5 : 10,
        // Define ordem padrão de ordenação (primeira coluna, decrescente)
        order: [[0, 'desc']],
        // Adiciona opções de comprimento de página
        lengthMenu: isMobile ? 
            [[5, 10, 25], [5, 10, 25]] : 
            [[10, 25, 50, -1], [10, 25, 50, "Todos"]],
        // Configurações para dispositivos móveis
        dom: isMobile ? 
            "<'row'<'col-12'f>>" +
            "<'row'<'col-12'tr>>" +
            "<'row'<'col-6'i><'col-6'p>>" :
            "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    };

    // Inicializa DataTables em todas as tabelas com a classe 'table-datatable'
    $('.table-datatable').each(function() {
        // Verifica se já não foi inicializado
        if (!$.fn.DataTable.isDataTable(this)) {
            // Obtém configurações específicas da tabela, se existirem
            let tableConfig = $(this).data('dt-config') || {};
            
            // Mescla configurações padrão com específicas
            const config = { ...defaultConfig, ...tableConfig };
            
            // Inicializa a tabela
            $(this).DataTable(config);
        }
    });
    
    // Ajustes específicos para tabelas responsivas em dispositivos móveis
    if (isMobile) {
        // Adiciona classe para identificar tabelas em dispositivos móveis
        $('.dataTables_wrapper').addClass('mobile-tables');
        
        // Ajusta altura das células para melhor visualização em toque
        $('.dataTable td, .dataTable th').css('padding', '0.5rem');
        
        // Ajusta filtro de pesquisa para ocupar largura total em mobile
        $('.dataTables_filter').css('width', '100%');
        $('.dataTables_filter input').css('width', 'calc(100% - 70px)');
        
        // Melhorar área de clique para botões de paginação
        $('.dataTables_paginate .paginate_button').css({
            'min-width': '40px',
            'min-height': '40px',
            'display': 'inline-flex',
            'align-items': 'center',
            'justify-content': 'center'
        });
    }
});