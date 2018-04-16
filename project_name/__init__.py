from datetime import datetime
from decimal import Decimal
from urllib.parse import quote_plus
from sqlalchemy import engine_from_config
from pyramid.config import Configurator
# from pyramid.request import Request, Response
from pyramid.renderers import JSON
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .controllers.security import SecurityRoot
from .Models import (
    DBSession,
    Base,
    dbConfig,
    )
from .Views import add_routes

from .pyramid_jwtauth import (
    JWTAuthenticationPolicy,
    includeme
    )


def datetime_adapter(obj, request):
    """Json adapter for datetime objects."""
    try:
        return obj.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return obj.strftime('%d/%m/%Y')


def decimal_adapter(obj, request):
    """Json adapter for Decimal objects.
    """
    return float(obj)


def bytes_adapter(obj, request):
    return base64.b64encode(obj).decode()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sqlalchemy.url'] = settings['cn.dialect'] + quote_plus(settings['sqlalchemy.url'])
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbConfig['url'] = settings['sqlalchemy.url']

    """ Configuration de la connexion à la BDD """
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Base.metadata.reflect(views=True)

    """ Configuration du serveur pyramid"""
    config = Configurator(settings=settings)
    # Add renderer for datetime objects
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)
    json_renderer.add_adapter(Decimal, decimal_adapter)
    json_renderer.add_adapter(bytes, bytes_adapter)
    config.add_renderer('json', json_renderer)

    # Set up authentication and authorization
    includeme(config)
    config.set_root_factory(SecurityRoot)

    # Set the default permission level to 'read'
    config.set_default_permission('read')
    config.include('pyramid_tm')
    add_routes(config)
    config.scan()
    return config.make_wsgi_app()
