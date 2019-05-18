from werkzeug.exceptions import HTTPException

from Bottle import create_app
from Bottle.errors.error import APIException
from errors.error_code import ServerError

app = create_app('development')

@app.errorhandler(Exception)
def framework_error(e):
    #raise e
    if isinstance(e, APIException):
        raise e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run()