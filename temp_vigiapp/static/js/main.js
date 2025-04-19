document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Format CPF inputs
    var cpfInputs = document.querySelectorAll('.cpf-input');
    cpfInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            if (value.length > 9) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{1,2}).*/, '$1.$2.$3-$4');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{3})(\d{3})(\d{1,3}).*/, '$1.$2.$3');
            } else if (value.length > 3) {
                value = value.replace(/^(\d{3})(\d{1,3}).*/, '$1.$2');
            }
            
            e.target.value = value;
        });
    });

    // Format CNPJ inputs
    var cnpjInputs = document.querySelectorAll('.cnpj-input');
    cnpjInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 14) {
                value = value.slice(0, 14);
            }
            
            if (value.length > 12) {
                value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{1,2}).*/, '$1.$2.$3/$4-$5');
            } else if (value.length > 8) {
                value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{1,4}).*/, '$1.$2.$3/$4');
            } else if (value.length > 5) {
                value = value.replace(/^(\d{2})(\d{3})(\d{1,3}).*/, '$1.$2.$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{1,3}).*/, '$1.$2');
            }
            
            e.target.value = value;
        });
    });

    // Format phone inputs
    var phoneInputs = document.querySelectorAll('.phone-input');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            if (value.length > 10) {
                value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,5})$/, '($1) $2');
            }
            
            e.target.value = value;
        });
    });

    // Format date inputs
    var dateInputs = document.querySelectorAll('.date-input');
    dateInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 8) {
                value = value.slice(0, 8);
            }
            
            if (value.length > 4) {
                value = value.replace(/^(\d{2})(\d{2})(\d{1,4}).*/, '$1/$2/$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{1,2}).*/, '$1/$2');
            }
            
            e.target.value = value;
        });
    });

    // Format time inputs
    var timeInputs = document.querySelectorAll('.time-input');
    timeInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 4) {
                value = value.slice(0, 4);
            }
            
            if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{1,2}).*/, '$1:$2');
            }
            
            e.target.value = value;
        });
    });

    // Auto-fill pessoa data when CPF is entered
    var pessoaLookupInputs = document.querySelectorAll('.pessoa-lookup');
    pessoaLookupInputs.forEach(function(input) {
        input.addEventListener('blur', function(e) {
            let cpf = e.target.value.replace(/\D/g, '');
            if (cpf.length === 11) {
                fetch('/pessoas/buscar-por-cpf/' + cpf)
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Pessoa não encontrada');
                    })
                    .then(data => {
                        // Fill form fields with pessoa data
                        let nomeInput = document.querySelector('#nome');
                        let telefoneInput = document.querySelector('#telefone');
                        let empresaInput = document.querySelector('#empresa');
                        
                        if (nomeInput) nomeInput.value = data.nome;
                        if (telefoneInput) telefoneInput.value = data.telefone;
                        if (empresaInput) empresaInput.value = data.empresa;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        });
    });

    // Auto-fill empresa data when CNPJ is entered
    var empresaLookupInputs = document.querySelectorAll('.empresa-lookup');
    empresaLookupInputs.forEach(function(input) {
        input.addEventListener('blur', function(e) {
            let cnpj = e.target.value.replace(/\D/g, '');
            if (cnpj.length === 14) {
                fetch('/empresas/buscar-por-cnpj/' + cnpj)
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Empresa não encontrada');
                    })
                    .then(data => {
                        // Fill form fields with empresa data
                        let nomeEmpresaInput = document.querySelector('#nome_empresa');
                        let telefoneEmpresaInput = document.querySelector('#telefone_empresa');
                        let coringaInput = document.querySelector('#coringa');
                        let nomeFuncInput = document.querySelector('#nome_func');
                        let telefoneFuncInput = document.querySelector('#telefone_func');
                        
                        if (nomeEmpresaInput) nomeEmpresaInput.value = data.nome_empresa;
                        if (telefoneEmpresaInput) telefoneEmpresaInput.value = data.telefone_empresa;
                        if (coringaInput) coringaInput.value = data.coringa;
                        if (nomeFuncInput) nomeFuncInput.value = data.nome_func;
                        if (telefoneFuncInput) telefoneFuncInput.value = data.telefone_func;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        });
    });

    // Handle delete confirmation modals
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('data-bs-target');
            const modal = new bootstrap.Modal(document.querySelector(target));
            modal.show();
        });
    });
});
