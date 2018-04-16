from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from sqlalchemy import select,delete
from ..Models import DBSession, User,Adress

@view_config(route_name='core/user',permission=NO_PERMISSION_REQUIRED,renderer='json')
def users(request):
    """Return the list of all the users with their ids.
    """
    query = select([
        User.id.label('PK_id'),
        User.Login.label('fullname')
    ]).where(User.HasAccess == True).order_by(User.Lastname, User.Firstname)
    return [dict(row) for row in DBSession.execute(query).fetchall()]


@view_config(route_name='core/user/id',permission=NO_PERMISSION_REQUIRED,renderer='json')
def getUser(request):
    ### récupération de l'id contenu dans l'url de la requête AJAX
    id_ = request.matchdict['id']

    """ 2 méthodes pour faire des requête, 
        utiliser l'ORM (1) 
        ou 
        via l'execution de requête SQL (2)"""
    
    """ (1) ORM : Retourne un objet User, avantage : utiliser les propriétés de l'objet """
    user = DBSession.query(User).get(id_) # car User.id est une primary key
    # ou DBSession.query(User).filter(User.id == id_).one()
    print(user.fullname)

    """ (2) Plusieurs manières de passer une requête SQL """

    """         (2.1) La requête brute: """
    stmtBrute = '''SELECT * FROM TUsers WHERE id='''+str(id_)
    resultBrute = DBSession.execute(stmtBrute).fetchone()  
    ### ici la methode fetchone() signifie que la requête ne doit nous retourné qu'un seul résultat (une seule ligne)

    print(resultBrute)

    """         (2.2) La requête construite avec sqlalchemy: """
    stmt = select([User]).where(User.id == id_) # ==> equivalent de la requête brute ecrite au dessus 
    # on peut aussi récupérer seulement les colonne qui nous interresse 
    # ex : select([User.id, User.Login]).where(User.id == id_)
    result = DBSession.execute(stmt).fetchall() 
    print(result)

    """         (2.3) On peut aussi acceder à la table TUsers via les metadonnées de l'objet Base,
                par exemple si la table n'est pas mappée en tant qu'objet de l'ORM """
    table = Base.metadata.tables['Tusers'] # on accede au colonne : table.c['id']
    otherStmt = select(table.c).where(table.c['id'] == id_)

    # ou encore select([table.c['id'],table.c['Login']])
    resultOther = DBSession.execute(otherStmt).fetchall()
    print(resultOther)


@view_config(route_name='core/user',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method='POST')
def addUser(request):

    # on recupere les données de la requête AJAX
    data = request.params

    data = {
    'Firstname':'toto',
    'Lastname' : 'tata',
    'Login' : 'totoTata',
    'Password': 'toto en force'
    }
    """ 2 methode encore : 
        utilisation de l'ORM (1)
        ou via une requête construite (2)
    """

    """ (1) Avantage on récupère l'id généré directement dans l'objet """
    # on instancie un objet User 
    newUser = User()
    # newUser.Login = data['Login']
    # newUser.Firstname = data['Firstname']
    # newUser.Lastname = data['Lastname']
    # newUser.Login = data['Login']
    # newUser.Password = data['Password']
    ## fastidieux :(, on préférera : 
    for key,value in data.items() :
        setattr(newUser,key,value)

    DBSession.add(newUser)
    DBSession.commit()
    print(newUser.id)

    """ (1.2) insert multiple : insert ligne par ligne :(  
        mais à l'avantage de récupéré les id dans chaque objet"""

    dataList = [{
    'Firstname':'khaled',
    'Lastname' : 'talbi',
    'Login' : 'kt',
    'Password': 'ktPWD'
    },
    {
    'Firstname':'fred',
    'Lastname' : 'berton',
    'Login' : 'fb',
    'Password': 'fbPWD'
    }]

    objectList = []
    for data in dataList:
        newUser = User()
        for key,value in data.items() :
            setattr(newUser,key,value)
        objectList.append(newUser)

    DBSession.add_all(objectList)
    DBSession.commit()
    for user in objectList:
        print(user.id)

    """ (1.2) insert multiple avec ORM : insert Block """
    dataList = [{
    'Firstname':'matheo',
    'Lastname' : 'jaouen',
    'Login' : 'mj',
    'Password': 'mjPWD'
    },
    {
    'Firstname':'gégé',
    'Lastname' : 'tibi',
    'Login' : 'gt',
    'Password': 'gtPWD'
    }]

    objectList = []
    for data in dataList:
        newUser = User()
        for key,value in data.items() :
            setattr(newUser,key,value)
        objectList.append(newUser)

    DBSession.bulk_save_objects(objectList)
    DBSession.commit()

    """ ou encore plus simplement : le plus performant """
    result = DBSession.bulk_insert_mappings(User,dataList)
    DBSession.commit()

    """ (2)  l'insert 1 row  (on préférera utilisé l'ORM)"""
    dataBis = {
    'Firstname':'olivier',
    'Lastname' : 'rovellotti',
    'Login' : 'The Boss',
    'Password': 'gourou'
    }
    insertStmt = User.__table__.insert(dataBis)
    print(insertStmt)
    DBSession.execute(insertStmt)
    DBSession.commit()

    """ (2.2) l'insert Block  """
    dataList = [{
    'Firstname':'tom',
    'Lastname' : 'lopez',
    'Login' : 'tl',
    'Password': 'tlPWD'
    },
    {
    'Firstname':'david',
    'Lastname' : 'lassagne',
    'Login' : 'dl',
    'Password': 'dlPWD'
    }]

    insertBlockStmt = User.__table__.insert(values=dataList,returning=[User.__table__.c.id])
    print(insertBlockStmt)
    result = DBSession.execute(insertBlockStmt).fetchall()

    print([row['id'] for row in result])
    DBSession.commit()

@view_config(route_name='core/user/id',permission=NO_PERMISSION_REQUIRED,renderer='json', request_method = 'DELETE')
def deleteUser(request):

    id_ = request.matchdict['id']
    """ Delete avec ORM """
    # curUser = DBSession.query(User).get(id_)
    # DBSession.delete(curUser)
    # DBSession.commit()

    """ ou  encore """
    # DBSession.query(User).filter_by(id=id_).delete()
    # DBSession.commit()

    """ en requete """ 
    # stmt = delete(User).where(User.id == id_)
    # DBSession.execute(stmt)
    # DBSession.commit()


