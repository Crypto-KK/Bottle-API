import functools
from collections import namedtuple

from flask import current_app, g, request
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature,\
    SignatureExpired
from flask_httpauth import HTTPTokenAuth
from Bottle.errors.error_code import AuthFailed, Forbidden, AppKeyError
from Bottle.models.user import User as UserModel
from Bottle.utils.scope import has_permission


auth = HTTPTokenAuth(scheme='JWT')
User = namedtuple('User', ['uid', 'scope'])

@auth.verify_token
def verify_token(token):
    '''token认证'''
    s = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY']
    )
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token不正确')
    except SignatureExpired:
        raise AuthFailed(msg='token过期')

    uid = data['uid']
    scope = data['scope']
    user = User(uid, scope)
    allow = has_permission(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    if user:
        g.current_user = user
        return True
    return False


def appkey_require(f):
    '''验证appkey是否正确'''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'AppKey' in request.headers:
            appkey = request.headers['AppKey']
            user = UserModel.query.filter_by(app_key=appkey).first()
            if user:
                return f(*args, **kwargs)
            else:
                raise AppKeyError()
    return wrapper



def auto_load_token(token):
    '''用户不需要自己处理异常'''
    s = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY']
    )
    try:
        data = s.loads(token, return_header=True)
    except BadSignature:
        raise AuthFailed(msg='token不正确')
    except SignatureExpired:
        raise AuthFailed(msg='token过期')
    return data


def generate_auth_token(uid, scope=None, exp=7200):
    '''
    生成令牌
    '''
    s = TimedJSONWebSignatureSerializer(
        current_app.config['SECRET_KEY'],
        expires_in=exp
    )
    return s.dumps({
        'uid': uid,
        'scope': scope
    })