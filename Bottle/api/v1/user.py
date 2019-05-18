from flask import jsonify, render_template, request

from Bottle.utils.redprint import Redprint
from Bottle.models.user import User
from Bottle.forms.user import UserRegisterForm
from Bottle.errors.error_code import CreateSuccess

api = Redprint('user')

@api.route('/register', methods=['POST'])
def register():
    '''
    用户注册
    '''
    form = UserRegisterForm().validate_for_api()
    User.register(
        form.nickname.data,
        form.email.data,
        form.password.data
    )
    return CreateSuccess()