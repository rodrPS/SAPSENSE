from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import math
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def gerar_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='recuperar-senha')

def validar_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='recuperar-senha', max_age=expiration)
        return email
    except Exception:
        return None

def str_to_bool(valor):
    return valor.lower() == 'sim'

def calcular_saps3(dados):
    """
    Calcula a pontuação SAPS 3 e a estimativa de mortalidade.
    A lógica é baseada no script de referência fornecido.
    """
    score = 16  # Pontuação base

    # 1. Idade
    data_nascimento_str = dados.get('data_nascimento', "Sun, 01 Jan 1900 00:00:00 GMT")
    data_admissao_str = dados.get('data_admissao', "Sun, 01 Jan 1900 00:00:00 GMT")
    data_nascimento = datetime.strptime(data_nascimento_str, "%a, %d %b %Y %H:%M:%S GMT").date()
    data_admissao = datetime.strptime(data_admissao_str, "%a, %d %b %Y %H:%M:%S GMT").date()
    idade = (data_admissao - data_nascimento).days / 365.25

    if idade >= 80: score += 18
    elif idade >= 75: score += 15
    elif idade >= 70: score += 13
    elif idade >= 60: score += 9
    elif idade >= 40: score += 5

    # Mapeamentos de pontos
    local_previo_pts = {'pronto-socorro/emergencia': 5, 'uti': 7, 'ala': 8}
    comorbidades_pts = {
        'terapia_cancer': 3, 'cancer_metastatico': 11,
        'insuficiencia_cardiaca': 6, 'cirrose': 8, 'aids': 8
    }
    motivos_admissao_pts = {
        'CARDIO/NEURO: DISTURBIOS DO RITMO CARDIACO': -5, 'CARDIO/NEURO: CONVULSOES': -4,
        'CARDIO: CHOQUE HIPOVOLEMICO (HEMORRAGICO OU NAO)': 3, 'CARDIO: CHOQUE SEPTICO': 5,
        'CARDIO: CHOQUE ANAFILATICO/MISTO OU INDEFINIDO': 5,
        'NEURO: COMA/ESTUPOR/CONFUSAO/AGITAÇAO/DELIRIUM/DISTÚRBIOS SONO–VIGILIA': 4,
        'NEURO: DEFICIT NEUROLOGICO FOCAL': 7, 'NEURO: EFEITO DE MASSA INTRACRANIANA': 10,
        'DIGESTIVO: ABDOMEN AGUDO/OUTR': 3, 'DIGESTIVO: PANCREATITE SEVERA': 9,
        'HEPATO: INSUFICIENCIA HEPATICA': 6
    }
    tipo_cirurgia_pts = {'CIRURGIA DE EMERGENCIA': 6, 'sem_cirurgia': 5}
    sitio_atomico_pts = {
        'CIRURGIA DE TRANSPLANTE': -11, 'CIRURGIA DE TRAUMA': -8,
        'CIRURGIA CARDIACA (REVASCULARIZAÇÃO)': -6, 'NEUROCIRURGIA': 5
    }
    tipo_infeccao_pts = {'NOSOCOMIAL': 4, 'RESPIRATORIA': 5}
    glasgow_pts = {'3-4': 15, '5': 10, '6': 7, '7-12': 2}
    bilirrubina_pts = {'2.0-5.9': 4, '>6.0': 5}
    creatinina_pts = {'1.2-1.9': 2, '2.0-3.4': 7, '>=3.5': 8}
    fc_pts = {'120-159': 5, '>=159': 7}
    pas_pts = {'70-119': 3, '40-69': 8, '<40': 11}
    plaquetas_pts = {'50000-99000': 5, '20000-49000': 8, '<20000': 13}
    oxigenacao_pts = {
        'PaO2<60_sem_VM': 5, 'PaO2FIO2>=100_com_VM': 7, 'PaO2FIO2<100_com_VM': 11
    }

    # Pontuações
    score += local_previo_pts.get(dados.get('local_previo', ''), 0)
    for k, v in comorbidades_pts.items():
        if str_to_bool(dados.get(k, 'nao')):
            score += v
    if str_to_bool(dados.get('drogas_vasoativas', 'nao')): score += 3
    if not str_to_bool(dados.get('admissao_planejada', 'sim')): score += 3

    # Motivos de admissão (com regra especial)
    motivos = dados.get('motivos_admissao', [])
    if 'CARDIO/NEURO: DISTURBIOS DO RITMO CARDIACO' in motivos and 'CARDIO/NEURO: CONVULSOES' in motivos:
        motivos.remove('CARDIO/NEURO: DISTURBIOS DO RITMO CARDIACO')
    for motivo in motivos:
        score += motivos_admissao_pts.get(motivo, 0)

    # Cirurgia
    if not str_to_bool(dados.get('cirurgia_realizada', 'sim')):
        score += tipo_cirurgia_pts.get('sem_cirurgia', 0)
    else:
        score += tipo_cirurgia_pts.get(dados.get('tipo_cirurgia', ''), 0)
        score += sitio_atomico_pts.get(dados.get('sitio_atomico', ''), 0)
    
    # Infecção
    if str_to_bool(dados.get('infeccao_aguda', 'nao')):
        score += tipo_infeccao_pts.get(dados.get('tipo_infeccao', ''), 0)

    # Dados categorizados
    score += glasgow_pts.get(dados.get('glasgow', ''), 0)
    score += bilirrubina_pts.get(dados.get('bilirrubina', ''), 0)
    if dados.get('temperatura') == '<35': score += 7
    score += creatinina_pts.get(dados.get('creatinina', ''), 0)
    score += fc_pts.get(dados.get('frequencia_cardiaca', ''), 0)
    if dados.get('leucocitos') == '>=15000': score += 2
    if dados.get('ph') == '<7.25': score += 3
    score += plaquetas_pts.get(dados.get('plaquetas', ''), 0)
    score += pas_pts.get(dados.get('pressao_sistolica', ''), 0)
    score += oxigenacao_pts.get(dados.get('oxigenacao', ''), 0)

    # Cálculo da mortalidade
    try:
        x = -32.6659 + math.log(score + 20.5958) * 7.3068
        mortalidade = (math.exp(x) / (1 + math.exp(x))) * 100
    except (ValueError, OverflowError):
        mortalidade = 0.0

    return score, mortalidade