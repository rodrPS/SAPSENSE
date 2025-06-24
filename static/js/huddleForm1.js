document.addEventListener('DOMContentLoaded', function() {
    const equipeCompareceuRadios = document.querySelectorAll('input[name="equipe_compareceu"]');
    const submitButton = document.getElementById('submit-huddle');
    const resumoDetalhadoSections = document.querySelectorAll('.resumo-detalhado');

    function checkEquipeCompareceu() {
        let equipeCompareceuValue = '';
        equipeCompareceuRadios.forEach(radio => {
            if (radio.checked) {
                equipeCompareceuValue = radio.value;
            }
        });

        if (equipeCompareceuValue === 'nao') {
            resumoDetalhadoSections.forEach(section => {
                section.classList.add('hidden');
            });
            if (submitButton) {
                submitButton.textContent = 'Enviar';
            }
        } else {
            resumoDetalhadoSections.forEach(section => {
                section.classList.remove('hidden');
            });
            if (submitButton) {
                submitButton.textContent = 'Próximo';
            }
        }
    }

    equipeCompareceuRadios.forEach(radio => {
        radio.addEventListener('change', checkEquipeCompareceu);
    });

    checkEquipeCompareceu();
});
