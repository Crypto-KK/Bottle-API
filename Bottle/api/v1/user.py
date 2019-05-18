from flask import jsonify, render_template

from Bottle.utils.redprint import Redprint
from Bottle.models.user import User


api = Redprint('user')

@api.route('', methods=['GET'])
def get_user():

    return 'asdf'