from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Sequence,
    String,
    func,
    Boolean,
    ForeignKey
    )

from sqlalchemy.ext.hybrid import hybrid_property
from ..Models import Base, dbConfig
from sqlalchemy.orm import relationship, backref

class Adress(Base):
    __tablename__ = 'Adresses'
    id = Column(Integer, primary_key=True)
    FK_user = Column(Integer, ForeignKey('TUsers.id') ,nullable=False)
    Adress = Column(String(250))
    City = Column(String(250))
    Country = Column(String(250))
    CreationDate = Column(DateTime, nullable=False,server_default=func.now())
    ModificationDate = Column(DateTime, nullable=False,server_default=func.now())

    User = relationship('User')

