from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

### Create a database session : one for the whole application
DBSession = scoped_session(sessionmaker())
Base = declarative_base()
dbConfig = {
    'dialect': 'mssql',
}

from .User import User
from .Adress import Adress
