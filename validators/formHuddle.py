from models import Huddle
from extensions import db

def processar_huddle_basico(step1_data):
    """Salva um Huddle com dados mínimos (caso equipe não tenha comparecido)."""
    huddle = Huddle(
        turno=step1_data.get('turno'),
        equipe_compareceu=step1_data.get('equipe_compareceu'),
        equipe_huddle=[],
        tecnicos_enfermagem=None,
        ha_leitos_bloqueados=None,
        qtd_leitos_bloqueados=None,
        motivo_bloqueio=None,
        altas_confirmadas=None,
        altas_aval=None,
        houve_solicitacao_vaga=None,
        qtd_solicitacoes=None,
        origem_solicitacoes=None,
        exames_programados=None,
        qtd_exames=None,
        quais_exames=None,
        mais_graves=None,
        em_isolamento=None,
        em_dialise=None,
        usando_svd=None,
        usando_cvc=None,
        retirada_svd=None,
        pacientes_retirada_svd=None,
        retirada_cvc=None,
        pacientes_retirada_cvc=None,
        despertar_diario=None,
        pacientes_despertar_diario=None,
        ventilacao_mecanica=None,
        ims_maior_igual_4=None,
        progressao_funcional=None,
        evento_adverso=None,
        problema_unidade=None,
        descricao_unidade=None,
        problema_hospital=None,
        descricao_hospital=None,
        outro_problema=None
    )
    db.session.add(huddle)
    db.session.commit()
    return huddle

def processar_huddle_completo(dados):
    """Salva um Huddle com todos os dados do formulário."""
    huddle = Huddle(
        turno=dados.get('turno'),
        equipe_compareceu=dados.get('equipe_compareceu'),
        equipe_huddle=dados.get('equipe_huddle', []),
        tecnicos_enfermagem=dados.get('tecnicos_enfermagem'),

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
