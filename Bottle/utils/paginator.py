from flask import current_app, request

def get_limit_offset_data(obj):
    '''
    获取分页数据，使用limit和offset
    obj: 数据模型
    '''
    offset = request.args.to_dict().get('offset', 0)
    limit = request.args.to_dict().get('limit', current_app.config['MAX_PER_PAGE'])
    if int(limit) > current_app.config['MAX_PER_PAGE']:
        limit = current_app.config['MAX_PER_PAGE']
    return obj.query.offset(offset).limit(limit).all()