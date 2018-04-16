from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from sqlalchemy import select,delete,join
from ..Models import DBSession, User,Adress


@view_config(route_name='core/user/adress',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method='POST')
def addUserWithAdress(request):

    # on recupere les données de la requête AJAX
    data = request.params

    dataUser = {
    'Firstname':'toto',
    'Lastname' : 'tata',
    'Login' : 'totoTata',
    'Password': 'toto en force'
    }

    dataAdress = [{
    'Adress' : '68 rue Sainte',
    'City' : 'Marseille',
    'Country' : 'France'
    },{
    'Adress' : '15 avenue Boulevard',
    'City' : 'Paris',
    'Country' : 'France'
    }]

    newUser = User()
    for key,value in dataUser.items() :
        setattr(newUser,key,value)

    listAdress = []
    for adress in dataAdress: 
        newAdress = Adress()
        for key,value in adress.items() :
            setattr(newAdress,key,value)
        listAdress.append(newAdress)

    newUser.Adresses = listAdress
    DBSession.add(newUser)
    DBSession.commit()


@view_config(route_name='core/user/id/adress',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method='GET')
def getUserWithAdress(request):

    id_ = request.matchdict['id']
    curUser = DBSession.query(User).get(id_)

    for adress in curUser.Adresses :
        print(adress.__dict__)



@view_config(route_name='core/user/adress',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method='GET')
def ListUserWithAdress(request):

    """ Avec Orm retourne des Objets User """ 
    userInMarseille = DBSession.query(User).join(User.Adresses).filter(Adress.City == 'Marseille').all()
    print (userInMarseille)


    " en requete "
    query = select([User,Adress]).where(User.id == Adress.FK_user).where(Adress.City == 'Paris')
    print(DBSession.execute(query).fetchall())

    " en requete 2 "
    table = join(User,Adress,User.id == Adress.FK_user)
    query = select([User,Adress]).select_from(table).where(Adress.City == 'Paris')
    print(DBSession.execute(query).fetchall())

    query2 = select([table]).select_from(table).where(Adress.City == 'Paris')
    print(DBSession.execute(query2).fetchall())


@view_config(route_name='core/adress/id',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method='GET')
def AdressWithUser(request):

    id_ = request.matchdict['id']
    curAdress = DBSession.query(Adress).get(id_)
    print(curAdress.User.__dict__)
