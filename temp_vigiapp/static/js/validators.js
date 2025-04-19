// CPF validation
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    
    if (cpf.length !== 11) {
        return false;
    }
    
    // Check if all digits are the same
    if (/^(\d)\1+$/.test(cpf)) {
        return false;
    }
    
    // Validate first digit
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let remainder = sum % 11;
    let digit = remainder < 2 ? 0 : 11 - remainder;
    
    if (parseInt(cpf.charAt(9)) !== digit) {
        return false;
    }
    
    // Validate second digit
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    remainder = sum % 11;
    digit = remainder < 2 ? 0 : 11 - remainder;
    
    if (parseInt(cpf.charAt(10)) !== digit) {
        return false;
    }
    
    return true;
}

// CNPJ validation
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]/g, '');
    
    if (cnpj.length !== 14) {
        return false;
    }
    
    // Check if all digits are the same
    if (/^(\d)\1+$/.test(cnpj)) {
        return false;
    }
    
    // Validate first digit
    let size = cnpj.length - 2;
    let numbers = cnpj.substring(0, size);
    let digits = cnpj.substring(size);
    let sum = 0;
    let pos = size - 7;
    
    for (let i = size; i >= 1; i--) {
        sum += parseInt(numbers.charAt(size - i)) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }
    
    let result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(0))) {
        return false;
    }
    
    // Validate second digit
    size = size + 1;
    numbers = cnpj.substring(0, size);
    sum = 0;
    pos = size - 7;
    
    for (let i = size; i >= 1; i--) {
        sum += parseInt(numbers.charAt(size - i)) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }
    
    result = sum % 11 < 2 ? 0 : 11 - sum % 11;
    if (result !== parseInt(digits.charAt(1))) {
        return false;
    }
    
    return true;
}

// Phone validation
function validarTelefone(telefone) {
    telefone = telefone.replace(/[^\d]/g, '');
    
    // Check if phone number has 10 or 11 digits
    return telefone.length === 10 || telefone.length === 11;
}

// Date validation
function validarData(data) {
    // Accept formats: DD/MM/YYYY
    const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = data.match(regex);
    
    if (!match) {
        return false;
    }
    
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10) - 1; // JS months are 0-indexed
    const year = parseInt(match[3], 10);
    
    const date = new Date(year, month, day);
    
    // Check if date is valid (not NaN) and day, month, year match what was entered
    return (
        !isNaN(date.getTime()) &&
        date.getDate() === day &&
        date.getMonth() === month &&
        date.getFullYear() === year
    );
}

// Time validation
function validarHora(hora) {
    // Accept formats: HH:MM
    const regex = /^([0-1][0-9]|2[0-3]):([0-5][0-9])$/;
    return regex.test(hora);
}

// Add form validation for all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            // Additional custom validations
            const cpfInput = form.querySelector('.cpf-input');
            if (cpfInput && cpfInput.value) {
                if (!validarCPF(cpfInput.value)) {
                    cpfInput.setCustomValidity('CPF inválido');
                    event.preventDefault();
                } else {
                    cpfInput.setCustomValidity('');
                }
            }
            
            const cnpjInput = form.querySelector('.cnpj-input');
            if (cnpjInput && cnpjInput.value) {
                if (!validarCNPJ(cnpjInput.value)) {
                    cnpjInput.setCustomValidity('CNPJ inválido');
                    event.preventDefault();
                } else {
                    cnpjInput.setCustomValidity('');
                }
            }
            
            const phoneInputs = form.querySelectorAll('.phone-input');
            phoneInputs.forEach(function(input) {
                if (input.value && !validarTelefone(input.value)) {
                    input.setCustomValidity('Telefone inválido');
                    event.preventDefault();
                } else {
                    input.setCustomValidity('');
                }
            });
            
            const dateInputs = form.querySelectorAll('.date-input');
            dateInputs.forEach(function(input) {
                if (input.value && !validarData(input.value)) {
                    input.setCustomValidity('Data inválida');
                    event.preventDefault();
                } else {
                    input.setCustomValidity('');
                }
            });
            
            const timeInputs = form.querySelectorAll('.time-input');
            timeInputs.forEach(function(input) {
                if (input.value && !validarHora(input.value)) {
                    input.setCustomValidity('Hora inválida');
                    event.preventDefault();
                } else {
                    input.setCustomValidity('');
                }
            });
            
            form.classList.add('was-validated');
        }, false);
    });
});
