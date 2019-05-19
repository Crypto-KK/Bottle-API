from datetime import datetime
from flask import jsonify, current_app, g

from Bottle.utils.auth import auth, auto_load_token, \
    generate_auth_token, appkey_require
from Bottle.utils.redprint import Redprint
from Bottle.models.user import User
from Bottle.forms.user import UserRegisterForm, EmailForm, \
    LoginForm, TokenForm
from Bottle.errors.error_code import CreateSuccess, VerifyCodeError, AuthFailed

from Bottle.utils.generate_key import generate_verify_code
from Bottle.utils.email import send_mail
from extensions import redis_conn, limiter

api = Redprint('user')


@api.route('/code/', methods=['POST'])
@limiter.limit("1 per minute")
def code():
    '''
    获取验证码接口
    POST -> /v1/code/
    :return {'code': "xxxx"}
    '''
    form = EmailForm().validate_for_api()
    email = form.email.data
    redis_conn.set(email, generate_verify_code())
    redis_conn.expire(email, current_app.config['REDIS_EXP'])
    return CreateSuccess()


@api.route('/register/', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    '''
    用户注册
    '''
    form = UserRegisterForm().validate_for_api()

    email = form.email.data
    code = redis_conn.get(email)

    if form.code.data == code.decode('utf-8'):
        User.register(
            form.nickname.data,
            email,
            form.password.data,
        )

        return CreateSuccess()

    return VerifyCodeError()


@api.route('/login/', methods=['POST'])
def login():
    '''登录'''
    form = LoginForm().validate_for_api()
    user_dict = User.verify(form.email.data, form.password.data)
    token = generate_auth_token(
        uid=user_dict['uid'],
        scope=user_dict['scope']
    )
    res = {
        'token': token.decode('utf-8')
    }
    return jsonify(res)


@api.route('/token/', methods=['POST'])
@auth.login_required
def get_token_info():
    '''获取令牌具体信息'''
    form = TokenForm().validate_for_api()
    data = auto_load_token(form.token.data)
    res = {
        'uid': data[0]['uid'],
        'scope': data[0]['scope'],
        'created_at': datetime.fromtimestamp(data[1]['iat']).strftime('%Y-%m-%d %H:%M:%S'),
        'expire_at': datetime.fromtimestamp(data[1]['exp']).strftime('%Y-%m-%d %H:%M:%S'),
    }

    return jsonify(res)


@api.route('/info/', methods=['GET'])
@auth.login_required
@limiter.limit("10 per minute")
def get_user_info():
    '''获得用户基本信息'''
    uid = g.current_user.uid
    user = User.query.get_or_404(uid)
    return jsonify(user)


@api.route('/info/<uid>/', methods=['GET'])
@auth.login_required
def admin_get_user_info(uid):
    '''admin获得用户基本信息'''
    user = User.query.get_or_404(uid)
    return jsonify(user)




@api.route('/get-app-key/', methods=['POST'])
@auth.login_required
def get_app_key():
    '''
    用户升级为开发者，获取appkey
    '''
    uid = g.current_user.uid
    User.register_developer(uid)
    return CreateSuccess()


