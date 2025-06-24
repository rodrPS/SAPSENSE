document.addEventListener('DOMContentLoaded', function () {
    const gruposCondicionais = [
        {
            trigger: 'problema_unidade',
            value: 'sim',
            targets: ['descricao_unidade']
        },
        {
            trigger: 'problema_hospital',
            value: 'sim',
            targets: ['descricao_hospital']
        }
    ];

    function atualizarCamposCondicionais() {
        gruposCondicionais.forEach(grupo => {
            const radios = document.querySelectorAll(`input[name="${grupo.trigger}"]`);
            let selecionado = '';
            radios.forEach(r => {
                if (r.checked) selecionado = r.value;
            });

            grupo.targets.forEach(id => {
                const campo = document.getElementById(id)?.closest('.form-group');
                const input = document.getElementById(id);

                if (campo && input) {
                    if (selecionado === grupo.value) {
                        campo.classList.remove('hidden');
                        input.setAttribute('required', 'required');
                    } else {
                        campo.classList.add('hidden');
                        input.removeAttribute('required');
                        input.value = '';
                    }
                }
            });
        });
    }

    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', atualizarCamposCondicionais);
    });

    atualizarCamposCondicionais();
});
