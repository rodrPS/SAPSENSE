document.addEventListener('DOMContentLoaded', function () {
    const gruposCondicionais = [
        {
            trigger: 'retirada_svd',
            value: 'sim',
            targets: ['pacientes_retirada_svd']
        },
        {
            trigger: 'retirada_cvc',
            value: 'sim',
            targets: ['pacientes_retirada_cvc']
        },
        {
            trigger: 'despertar_diario',
            value: 'sim',
            targets: ['pacientes_despertar_diario']
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
                        if (input.type === 'number' || input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                            input.value = '';
                        }
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
