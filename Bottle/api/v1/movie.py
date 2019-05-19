
from flask import jsonify, current_app, g, request

from Bottle.utils.auth import appkey_require
from Bottle.utils.redprint import Redprint
from Bottle.models.movie import HotMovie, NewMovie, ClassicMovie
from Bottle.forms.movie import MovieForm
from Bottle.errors.error_code import CreateSuccess, MovieTypeError
from extensions import limiter

api = Redprint('movies')


@api.route('/', methods=['GET'])
@appkey_require
@limiter.limit("500 per hour")
def get_movie_list():
    form = MovieForm(request.args)
    offset = request.args.to_dict().get('offset', 0)
    limit = request.args.to_dict().get('limit', current_app.config['MAX_PER_PAGE'])
    if form.type.data not in ['new', 'hot', 'classic']:
        return MovieTypeError()
    match = {
        'new': NewMovie,
        'hot': HotMovie,
        'classic': ClassicMovie
    }
    res = get_paginate_data(match[form.type.data], offset, limit)
    return jsonify(res)


def get_paginate_data(obj, offset, limit):
    if int(limit) > current_app.config['MAX_PER_PAGE']:
        limit = current_app.config['MAX_PER_PAGE']
    return obj.query.offset(offset).limit(limit).all()
