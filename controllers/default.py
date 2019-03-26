def login():
    return dict()

def loginProcess():
    email = request.vars.email
    password = request.vars.password
    if not auth.login_bare(email,password):
        redirect(URL('login'))
    redirect(URL('dashboard'))

def register():
    return dict()

def registerProcess():
    firstName = request.vars.firstName
    lastName = request.vars.lastName
    email = request.vars.email
    submitted_pass = request.vars.password
    address = request.vars.address
    phone = request.vars.phone
    if not auth.register_bare(first_name=firstName,last_name=lastName,email=email, password=submitted_pass, address=address, phone=phone):
        print(submitted_pass)
        redirect(URL('register'))
    redirect(URL('login'))

@auth.requires_login()
def dashboard():
    # chores = db().select(db.chores.ALL)
    chores = db((db.chores.created_by==auth.user) & (db.chores.status=='unfinished')).select()
    return dict(chores=chores)

def viewFinishedChores():
    chores = db((db.chores.created_by==auth.user) & (db.chores.status=='finished')).select()
    return dict(chores=chores)

def addChore():
    form = crud.create(db.chores, next=URL('dashboard'), message = T("New Chore Added"))
    return dict(form=form)

def viewChore():
    form=crud.read(db.chores, request.args(0))
    return dict(form=form)

def editChore():
    form=crud.update(db.chores, request.args(0),  next=URL('dashboard'), message = "Chore Details Editted")
    return dict(form=form)

def deleteChore():
    crud.delete(db.chores, request.args(0),next=URL('dashboard'),message = "Loan Deleted")

def choreFinished():
    db((db.chores.id==request.args(0)) & (db.chores.status=='unfinished') ).update(status='finished')
    redirect(URL('dashboard'))

def choreNotFinished():
    db((db.chores.id==request.args(0)) & (db.chores.status=='finished') ).update(status='unfinished')
    redirect(URL('viewFinishedChores'))  

def userProfile():
    return dict(form=auth.profile())

def change_password():
    return dict(form=auth.change_password())

def logout():
    auth.logout()

def index():
    chores = db().select(db.chores.ALL)
    return dict(chores=chores)

def viewDetails():
    user=crud.read(db.auth_user,request.args(1) )
    chore=crud.read(db.chores, request.args(0))
    return dict(user=user,chore=chore)

@auth.requires_membership('admin')
def manage():
    grid = SQLFORM.smartgrid(db.chores)
    return dict(grid=grid)
