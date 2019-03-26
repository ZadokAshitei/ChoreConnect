from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon.tools import Crud
configuration = AppConfig(reload=True)

db= DAL("sqlite://storage.sqlite")
crud = Crud(db)
crud.settings.controller = 'default'
crud.messages.record_updated = 'Record Updated'

auth = Auth(db)
auth.settings.login_next = URL('index')
auth.settings.logout_next = URL('login')
auth.settings.login_url = URL('login')
auth.settings.register_next = URL('login')
auth.settings.extra_fields['auth_user']=[
    Field('address'),
    Field('phone')
]
auth.define_tables()

db.define_table('chores',
                Field('choreName'),
                Field('choreDescription'),
                Field('choreDuration'),
                Field('choreLocation'),
                Field('chorePrice'),
                Field('status'),
                auth.signature)

def getUserByid(id):
    user=db.auth_user(id)
    return user.first_name + ' ' + user.last_name
