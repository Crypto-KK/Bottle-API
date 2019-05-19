class Scope:
    allow_api = []
    allow_module = []
    excluded = []

    def __add__(self, other):
        self.allow_api += other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module += other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.excluded += other.excluded
        self.excluded = list(set(self.excluded))
        return self


class UserScope(Scope):
    '''普通用户权限'''
    allow_api = ['v1.user+get_token_info', 'v1.user+get_user_info',
                 'v1.user+get_app_key']


class DeveloperScope(Scope):
    '''开发者权限'''

    def __init__(self):
        self + UserScope()


class AdminScope(Scope):
    '''管理员权限'''
    allow_api = ['v1.user+admin_get_user_info']

    def __init__(self):
        self + DeveloperScope()


class SuperScope(Scope):
    '''超级用户权限'''
    allow_module = ['v1.user']


if __name__ == '__main__':
    print(AdminScope().allow_api)


def has_permission(scope, endpoint):
    scope = globals()[scope]()
    red_name = endpoint.split('+')[0]
    print(endpoint)
    if endpoint in scope.excluded:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
