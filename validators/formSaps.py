from flask import session
from datetime import datetime
from models import db, Paciente, Internacao
from utils import str_to_bool
from sqlalchemy.exc import SQLAlchemyError

class FormularioIncompletoException(Exception):
    """Erro de preenchimento do formulário SAPS 3."""
    pass


def obter_dados_formulario():
    dados = {}
    for step in ['step1', 'step2', 'step3', 'step4']:
        dados.update(session.get(step, {}))

    campos_obrigatorios = [
        'cpf', 'nome', 'leito', 'data_nascimento', 'procedencia', 'data_admissao', 'reinternacao',
        'duracao_internacao', 'local_previo', 'terapia_cancer', 'cancer_metastatico',
        'insuficiencia_cardiaca', 'cirrose', 'aids', 'drogas_vasoativas',
        'admissao_planejada', 'motivos_admissao', 'cirurgia_realizada', 'infeccao_aguda',
        'glasgow', 'temperatura', 'frequencia_cardiaca', 'pressao_sistolica',
        'bilirrubina', 'creatinina', 'leucocitos', 'ph', 'plaquetas', 'oxigenacao'
    ]

    campos_condicionais = []

    if dados.get('cirurgia_realizada') == 'sim':
        campos_condicionais += ['tipo_cirurgia', 'sitio_atomico']

    if dados.get('infeccao_aguda') == 'sim':
        campos_condicionais += ['tipo_infeccao']

    faltando = [campo for campo in campos_obrigatorios + campos_condicionais if not dados.get(campo)]
    if faltando:
        raise FormularioIncompletoException(
            f"Campos obrigatórios ausentes ou vazios: {', '.join(faltando)}"
        )

    if faltando:
        raise FormularioIncompletoException(
            f"Campos obrigatórios ausentes ou vazios: {', '.join(faltando)}"
        )

    return dados

def salvar_dados_saps(dados, saps_score, mortalidade_estimada):
    cpf = dados['cpf'].replace('.', '').replace('-', '')

    try:
        # 🔍 Paciente: cria ou atualiza
        paciente = Paciente.query.filter_by(cpf=cpf).first()

        if not paciente:
            paciente = Paciente(
                cpf=cpf,
                nome=dados['nome'],
                data_nascimento=dados['data_nascimento']
            )
            db.session.add(paciente)
        else:
            paciente.nome = dados['nome']
            paciente.data_nascimento = dados['data_nascimento']

        db.session.commit()

        # 🔍 Internação: busca ativa
        internacao = Internacao.query.filter_by(paciente_id=paciente.id, data_desfecho=None).first()

        campos_comuns = {
            'leito': dados['leito'],
            'procedencia': dados['procedencia'],
            'data_admissao': dados['data_admissao'],
            'reinternacao': str_to_bool(dados['reinternacao']),
            'duracao_internacao': dados.get('duracao_internacao'),
            'local_previo': dados.get('local_previo'),

            'terapia_cancer': str_to_bool(dados['terapia_cancer']),
            'cancer_metastatico': str_to_bool(dados['cancer_metastatico']),
            'insuficiencia_cardiaca': str_to_bool(dados['insuficiencia_cardiaca']),
            'cirrose': str_to_bool(dados['cirrose']),
            'aids': str_to_bool(dados['aids']),
            'drogas_vasoativas': str_to_bool(dados['drogas_vasoativas']),

            'admissao_planejada': str_to_bool(dados['admissao_planejada']),
            'motivos_admissao': ",".join(dados.get('motivos_admissao', [])),

            'cirurgia_realizada': str_to_bool(dados['cirurgia_realizada']),
            'tipo_cirurgia': dados.get('tipo_cirurgia'),
            'sitio_atomico': dados.get('sitio_atomico'),

            'infeccao_aguda': str_to_bool(dados['infeccao_aguda']),
            'tipo_infeccao': dados.get('tipo_infeccao'),

            'glasgow': dados['glasgow'],
            'temperatura': dados['temperatura'],
            'frequencia_cardiaca': dados['frequencia_cardiaca'],
            'pressao_sistolica': dados['pressao_sistolica'],
            'bilirrubina': dados['bilirrubina'],
            'creatinina': dados['creatinina'],
            'leucocitos': dados['leucocitos'],
            'ph': dados['ph'],
            'plaquetas': dados['plaquetas'],
            'oxigenacao': dados['oxigenacao'],
            'saps_score': saps_score,
            'mortalidade_estimada': mortalidade_estimada
        }

        if internacao:
            # ✏️ Atualiza internação ativa
            for campo, valor in campos_comuns.items():
                setattr(internacao, campo, valor)
        else:
            # 🆕 Cria nova internação
            internacao = Internacao(paciente_id=paciente.id, **campos_comuns)
            db.session.add(internacao)

        db.session.commit()
        return internacao

    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError(f"Erro ao salvar no banco de dados: {str(e)}")
