from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, TextAreaField, RadioField, DateField
from wtforms.validators import DataRequired, Optional

class InternacaoForm(FlaskForm):
    id = HiddenField()

    # Campos editáveis
    lpp_admissao = RadioField('LPP na Admissão?', choices=[('sim', 'Sim'), ('nao', 'Não')], validators=[DataRequired()])
    lpp_alta = RadioField('LPP na Alta?', choices=[('sim', 'Sim'), ('nao', 'Não')], validators=[Optional()])
    diagnostico_atual = TextAreaField('Procedimento / Diagnóstico Atual', validators=[Optional()])
    data_desfecho = DateField('Data de Desfecho', validators=[Optional()])
    desfecho = SelectField('Desfecho', choices=[('', 'Selecione'), ('alta', 'Alta'), ('obito', 'Óbito'), ('transferencia', 'Transferência')], validators=[Optional()])
    destino = SelectField('Destino', choices=[('', 'Selecione'), ('outra ala', 'Outra Ala'), ('outro hospital', 'Outro Hospital'), ('domicilio', 'Domicilio'), ('necroterio', 'Necrotério')], validators=[Optional()])

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        if self.desfecho.data and self.desfecho.data != "":
            if not self.data_desfecho.data:
                self.data_desfecho.errors.append("A data de desfecho é obrigatória quando há desfecho.")
                rv = False
            if not self.destino.data or self.destino.data == "":
                self.destino.errors.append("O destino é obrigatório quando há desfecho.")
                rv = False

            if not self.lpp_alta.data:
                self.lpp_alta.errors.append("Campo obrigatório quando o desfecho é alta.")
                rv = False

        return rv
