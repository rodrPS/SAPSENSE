document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('#equipe-compareceu-radio input[type="radio"]');
    const detalhes = document.getElementsByClassName("resumo-detalhado");
    const botao = document.getElementById("submit-huddle");

    function verificarSelecao() {
        const selecionado = [...radios].find(r => r.checked);
        if (selecionado && selecionado.value === "nao") {
            detalhes.forEach(d => d.classList.add('hidden'));
            botao.textContent = "Enviar";
        } else {
            detalhes.forEach(d => d.classList.remove('hidden'));
            botao.textContent = "Próximo";
        }
    }

    radios.forEach(r => r.addEventListener("change", verificarSelecao));
    verificarSelecao();
});
