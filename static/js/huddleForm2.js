document.addEventListener('DOMContentLoaded', function () {
    const gruposCondicionais = [
        {
            trigger: 'ha_leitos_bloqueados',
            value: 'sim',
            targets: ['qtd_leitos_bloqueados', 'motivo_bloqueio']
        },
        {
            trigger: 'houve_solicitacao_vaga',
            value: 'sim',
            targets: ['qtd_solicitacoes', 'origem_solicitacoes']
        },
        {
            trigger: 'exames_programados',
            value: 'sim',
            targets: ['qtd_exames', 'quais_exames']
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
