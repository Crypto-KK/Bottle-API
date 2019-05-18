from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):

    '''自定义api异常，默认错误码为999'''
    code = 500
    msg = '未知错误'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None):
        if code:
            self.code = code

        if msg:
            self.msg = msg

        if error_code:
            self.error_code = error_code

        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        return json.dumps(body)

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]



    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]

