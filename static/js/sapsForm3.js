function toggleCamposCirurgia() {
    const resposta = document.querySelector('input[name="cirurgia_realizada"]:checked');
    const campos = document.getElementById('cirurgia-campos');
    if (resposta && resposta.value === 'sim') {
        campos.classList.remove('hidden');
    } else {
        campos.classList.add('hidden');
    }
}

function toggleCampoInfeccao() {
    const resposta = document.querySelector('input[name="infeccao_aguda"]:checked');
    const campo = document.getElementById('infeccao-campo');
    if (resposta && resposta.value === 'sim') {
        campo.classList.remove('hidden');
    } else {
        campo.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    toggleCamposCirurgia();
    toggleCampoInfeccao();
});
