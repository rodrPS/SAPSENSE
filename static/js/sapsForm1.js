function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
    let soma = 0, resto;
    for (let i = 1; i <= 9; i++) soma += parseInt(cpf[i - 1]) * (11 - i);
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf[9])) return false;

    soma = 0;
    for (let i = 1; i <= 10; i++) soma += parseInt(cpf[i - 1]) * (12 - i);
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;

    return resto === parseInt(cpf[10]);
}

function aplicarMascaraCPF(input) {
    input.addEventListener("input", function () {
        let value = input.value.replace(/\D/g, '');

        value = value.substring(0, 11);

        if (value.length > 9) {
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, "$1.$2.$3-$4");
        } else if (value.length > 6) {
            value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, "$1.$2.$3");
        } else if (value.length > 3) {
            value = value.replace(/(\d{3})(\d{1,3})/, "$1.$2");
        }

        input.value = value;
    });
}

function inserirErroDepois(input, mensagem) {
    removerErrosAnteriores(input);
    const small = document.createElement('small');
    small.classList.add('text-danger');
    small.innerText = mensagem;
    input.insertAdjacentElement('afterend', small);
}

function removerErrosAnteriores(input) {
    const proximo = input.nextElementSibling;
    if (proximo && proximo.classList.contains('text-danger')) {
        proximo.remove();
    }
}

function validarNomeCompleto(nome) {
    const partes = nome.trim().split(/\s+/);
    const somenteLetras = /^[A-Za-zÀ-ÿ\s]+$/;

    return partes.length >= 2 && somenteLetras.test(nome);
}


window.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector("form");
    const cpfInput = document.querySelector('input[name="cpf"]');
    const nomeInput = document.querySelector('input[name="nome"]');

    aplicarMascaraCPF(cpfInput);

    cpfInput.addEventListener("blur", function () {
        removerErrosAnteriores(cpfInput);
        if (cpfInput.value.trim() !== "" && !validarCPF(cpfInput.value)) {
            inserirErroDepois(cpfInput, "CPF inválido.");
        }
    });

    nomeInput.addEventListener("blur", function () {
        removerErrosAnteriores(nomeInput);
        if (nomeInput.value.trim() !== "" && !validarNomeCompleto(nomeInput.value)) {
            inserirErroDepois(nomeInput, "Digite nome e sobrenome.");
        }
    });

    nomeInput.addEventListener("input", function () {
        this.value = this.value.replace(/[^A-Za-zÀ-ÿ\s]/g, "");
    });

    form.addEventListener("submit", function (e) {
        let valido = true;

        removerErrosAnteriores(cpfInput);
        removerErrosAnteriores(nomeInput);

        if (!validarCPF(cpfInput.value)) {
            inserirErroDepois(cpfInput, "CPF inválido.");
            valido = false;
        }

        if (!validarNomeCompleto(nomeInput.value)) {
            inserirErroDepois(nomeInput, "Digite nome e sobrenome.");
            valido = false;
        }

        if (!valido) {
            e.preventDefault();
        }
    });
});

