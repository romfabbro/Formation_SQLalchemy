from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Sequence,
    String,
    func,
    Boolean
    )

from sqlalchemy.ext.hybrid import hybrid_property
from ..Models import Base, dbConfig
from sqlalchemy.orm import relationship, backref



class User(Base):
    __tablename__ = 'TUsers'
    id = Column(Integer, primary_key=True)
    Lastname = Column(String(50), nullable=False)
    Firstname = Column(String(50), nullable=False)
    CreationDate = Column(DateTime, nullable=False,server_default=func.now())
    Login = Column(String(255), nullable=False)
    Password = Column(String(50), nullable=False)
    Language = Column(String(5))
    ModificationDate = Column(DateTime, nullable=False,server_default=func.now())
    HasAccess = Column(Boolean)

    Adresses = relationship('Adress')

    @hybrid_property
    def fullname(self):
        """ Return the fullname of a user.
        """
        return self.Lastname + ' ' + self.Firstname
    
    def check_password(self, given_pwd):
        """Check the password of a user.
        
        Parameters
        ----------
        given_pwd : string
            The password to check, assumed to be an SHA1 hash of the real one.
            
        Returns
        -------
        boolean
            Either the password matches or not
        """
        return self.Password == given_pwd.lower()
