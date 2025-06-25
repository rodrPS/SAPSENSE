# SAPSENSE/validators/formHuddle.py
from models import Huddle
from extensions import db

def processar_huddle_basico(step1_data):
    """Salva um Huddle com dados mínimos (caso equipe não tenha comparecido)."""
    huddle = Huddle(
        turno=step1_data.get('turno'),
        equipe_compareceu=step1_data.get('equipe_compareceu')
        # Os demais campos já possuem default=0 ou None no modelo
    )
    db.session.add(huddle)
    db.session.commit()
    return huddle

def processar_huddle_completo(dados):
    """Salva um Huddle com todos os dados do formulário."""
    huddle = Huddle(
        # Step 1
        turno=dados.get('turno'),
        equipe_compareceu=dados.get('equipe_compareceu'),
        tecnicos_enfermagem=dados.get('tecnicos_enfermagem', 0),
        qtd_medicos=dados.get('qtd_medicos', 0),
        qtd_direcao=dados.get('qtd_direcao', 0),
        qtd_enfermeiros=dados.get('qtd_enfermeiros', 0),
        qtd_nucleo_seguranca=dados.get('qtd_nucleo_seguranca', 0),
        qtd_fisioterapeutas=dados.get('qtd_fisioterapeutas', 0),
        qtd_nutricionistas=dados.get('qtd_nutricionistas', 0),
        qtd_fonoaudiologos=dados.get('qtd_fonoaudiologos', 0),
        qtd_coras=dados.get('qtd_coras', 0),
        qtd_assistente_social=dados.get('qtd_assistente_social', 0),
        qtd_nir=dados.get('qtd_nir', 0),

        # Step 2
        ha_leitos_bloqueados=dados.get('ha_leitos_bloqueados'),
        qtd_leitos_bloqueados=dados.get('qtd_leitos_bloqueados'),
        motivo_bloqueio=dados.get('motivo_bloqueio'),
        altas_confirmadas=dados.get('altas_confirmadas'),
        altas_aval=dados.get('altas_aval'),
        houve_solicitacao_vaga=dados.get('houve_solicitacao_vaga'),
        qtd_solicitacoes=dados.get('qtd_solicitacoes'),
        origem_solicitacoes=dados.get('origem_solicitacoes'),
        exames_programados=dados.get('exames_programados'),
        qtd_exames=dados.get('qtd_exames'),
        quais_exames=dados.get('quais_exames'),

        # Step 3
        mais_graves=dados.get('mais_graves'),
        em_isolamento=dados.get('em_isolamento'),
        em_dialise=dados.get('em_dialise'),
        usando_svd=dados.get('usando_svd'),
        usando_cvc=dados.get('usando_cvc'),
        retirada_svd=dados.get('retirada_svd'),
        pacientes_retirada_svd=dados.get('pacientes_retirada_svd'),
        retirada_cvc=dados.get('retirada_cvc'),
        pacientes_retirada_cvc=dados.get('pacientes_retirada_cvc'),
        despertar_diario=dados.get('despertar_diario'),
        pacientes_despertar_diario=dados.get('pacientes_despertar_diario'),
        ventilacao_mecanica=dados.get('ventilacao_mecanica'),
        ims_maior_igual_4=dados.get('ims_maior_igual_4'),
        progressao_funcional=dados.get('progressao_funcional'),

        # Step 4
        evento_adverso=dados.get('evento_adverso'),
        problema_unidade=dados.get('problema_unidade'),
        descricao_unidade=dados.get('descricao_unidade'),
        problema_hospital=dados.get('problema_hospital'),
        descricao_hospital=dados.get('descricao_hospital'),
        outro_problema=dados.get('outro_problema')
    )
    db.session.add(huddle)
    db.session.commit()
    return huddle