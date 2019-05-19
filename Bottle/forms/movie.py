from Bottle.forms.base import BaseForm
from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import Length, DataRequired, ValidationError



class MovieForm(Form):
    type = StringField(
        validators=[DataRequired(message='类型不能为空')]
    )



