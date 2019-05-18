from Bottle.forms.base import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Length, DataRequired, Email, Regexp, ValidationError
from Bottle.models.user import User


class UserRegisterForm(BaseForm):
    email = StringField(
        validators=[DataRequired(message='邮箱不能为空'), Email()]
    )
    password = StringField(
        validators=[DataRequired(message='密码不能为空')]
    )

    nickname = StringField(
        validators=[DataRequired(message='昵称不能为空'), Length(min=2, max=20)]
    )

    def validate_email(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message='邮箱重复')

    def validate_nickname(self, value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError(message='昵称重复')
