from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ..Models import DBSession, User
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.response import Response

import transaction

route_prefix = 'security/'

@view_config(route_name=route_prefix+'has_access')
def has_access(request):
    return request.response
