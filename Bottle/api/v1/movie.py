
from flask import jsonify, current_app, g, request

from Bottle.utils.auth import appkey_require
from Bottle.utils.redprint import Redprint
from Bottle.models.movie import HotMovie, NewMovie, ClassicMovie
from Bottle.forms.movie import MovieForm
from Bottle.errors.error_code import CreateSuccess, MovieTypeError
from extensions import limiter
from Bottle.utils.paginator import get_limit_offset_data

api = Redprint('movies')


@api.route('/', methods=['GET'])
@appkey_require
@limiter.limit("500 per hour")
def get_movie_list():
    form = MovieForm(request.args)
    if form.type.data not in ['new', 'hot', 'classic']:
        return MovieTypeError()
    match = {
        'new': NewMovie,
        'hot': HotMovie,
        'classic': ClassicMovie
    }
    res = get_limit_offset_data(match[form.type.data])
    return jsonify(res)




