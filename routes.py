from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from jinja2 import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

routes = Blueprint('routes', __name__, template_folder='templates')

db = SQLAlchemy()
sess = Session()

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('ADMIN', 'STAFF'), nullable=False)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String, nullable=False)

@routes.errorhandler(Exception) # Website error handler
def error(error):
    return render_template('shared/error.html', error=error), 500

@routes.route('/', defaults={'page':'index'}, methods=['GET', 'POST'])
@routes.route('/<page>', methods=['GET', 'POST'])
def show(page):
    if page == 'index': 
        if request.method == 'POST':
            print("""\n 
            POST METHOD CALLED
            Name: {} 
            Email: {}
            Message: {} \n""".format(request.form.get('name'), request.form.get('email'), request.form.get('message')))

            toCommit = Messages(name = request.form.get('name'), email = request.form.get('email'), message = request.form.get('message'))
            db.session.add(toCommit)
            db.session.commit()

        for message in Messages.query.all():
            print(f"ID: {message.id} | Name: {message.name} | Email: {message.email} | Message: {message.message}")
    
    if page == 'auth':
        if request.method == 'POST':
            print("""\n 
            POST METHOD CALLED
            Username: {} 
            Password: {}\n""".format(request.form.get('username'), request.form.get('password')))

            if request.form.get('username'):
                if Auth.query.filter_by(username = request.form.get('username')).filter_by(password = request.form.get('password')).first():
                    session['username'] = request.form.get('username')
                    return redirect('/dashboard')
                else:
                    session['errormsg'] = ["Credenciais Inválidas!", "Verifique os campos e tente novamente."]
    
    if page == 'registo':
        if request.method == 'POST':
            if request.form.get('username'):
                print("""\n 
            POST METHOD CALLED
            Name: {} 
            Email: {}
            Username: {}
            Password: {}
            Repeat-Password: {}\n""".format(request.form.get('name'), request.form.get('email'), request.form.get('username'), request.form.get('password'), request.form.get('repeat-password')))
                
                if Auth.query.filter_by(email = request.form.get('email')):
                    session['errormsg'] = ["Este email já existe", "Este email já foi registado."]
                    return redirect('/registo')
                
                if Auth.query.filter_by(email = request.form.get('username')):
                    session['errormsg'] = ["Este nome de utilizador já existe", "Este nome de utilizador já foi registado."]
                    return redirect('/registo')
                
                if request.form.get('password') == request.form.get('repeat-password'):
                    session['errormsg'] = ["As senhas não são iguais.", "Verifique os campos e tente novamente."]
                    return redirect('/registo')

                toCommit = Auth(username = request.form.get('username'), name = request.form.get('name'), password = request.form.get('password'), email = request.form.get('email'))
                db.session.add(toCommit)
                db.session.commit()
                print(f'\n[INFO] Utilizador {request.form.get("username")} adicionado à base de dados (Registo).\n')

    
    if page == 'dashboard':
        if session.get('username') is None:
            return redirect('/auth')

        user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
        return render_template('dashboard.html', user=user)
    
    if page == 'logout':
        if session:
            session.pop('username', None)
        
        return redirect('/')
    
    if page == 'messages':
        messages = Messages.query.all()
        return render_template('messages.html', messages=messages)
    
    if page == 'clear_cookie':
        data = request.get_json()
        new_value = data.get('new_value')

        session['errormsg'] = new_value
        return 'Error cookie new value: {}'.format(session['errormsg'])
                
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        raise(Exception('Não conseguimos localizar esta página. Código de erro: PAGE_NOT_FOUND'))