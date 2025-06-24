from models import db, Internacao
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class AtualizacaoInternacaoInvalida(Exception):
    """Erro ao atualizar os dados da internação."""
    pass


def atualizar_internacao_com_formulario(form):
    try:
        internacao_id = form.id.data
        internacao = Internacao.query.get(internacao_id)

        if not internacao:
            raise AtualizacaoInternacaoInvalida("Internação não encontrada.")

        internacao.lpp_admissao = form.lpp_admissao.data == 'sim'
        internacao.diagnostico_atual = form.diagnostico_atual.data
        internacao.data_desfecho = form.data_desfecho.data or None
        internacao.desfecho = form.desfecho.data or None
        internacao.destino = form.destino.data or None
        internacao.lpp_alta = form.lpp_alta.data == 'sim' or None
        internacao.data_registro = datetime.utcnow() or None

        db.session.commit()
        return internacao

    except SQLAlchemyError as e:
        db.session.rollback()
        raise AtualizacaoInternacaoInvalida("Erro ao salvar no banco de dados: " + str(e))
