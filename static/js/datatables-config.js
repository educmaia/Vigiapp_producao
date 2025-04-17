document.addEventListener('DOMContentLoaded', function() {
    // Initialize DataTables for all tables with class 'datatable'
    $('.datatable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json',
        },
        responsive: true,
        order: [[0, 'desc']],
        pageLength: 10,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "Todos"]],
        columnDefs: [{
            targets: 'no-sort',
            orderable: false
        }]
    });
});
