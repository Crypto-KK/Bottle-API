from Bottle.errors.error import APIException


class CreateSuccess(APIException):
    msg = 'ok'
    code = 201
    error_code = 0


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1000


class AuthFailed(APIException):
    code = 401
    msg = '认证失败'
    error_code = 1002


class Forbidden(APIException):
    code = 403
    msg = '禁止访问,权限不足'
    error_code = 1003


class NotFound(APIException):
    code = 404
    msg = '资源未找到'
    error_code = 1001


class DeleteSuccess(CreateSuccess):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = '未知错误'
    error_code = 999


'''业务相关错误'''


class VerifyCodeError(APIException):
    code = 401
    msg = '验证码错误'
    error_code = 2001
