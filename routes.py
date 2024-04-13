from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime

routes = Blueprint('routes', __name__, template_folder='templates')

db   = SQLAlchemy()
sess = Session()

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('USER', 'ADMIN', 'STAFF'), nullable=False)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String, nullable=False)

@routes.errorhandler(Exception) # Website error handler
def error(error):
    return render_template('shared/error.html', error=error), 500

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_message = Messages(name = request.form.get('name'), email = request.form.get('email'), message = request.form.get('message'))
        db.session.add(new_message)
        db.session.commit()
    
    return render_template('index.html')

@routes.route('/auth', endpoint='auth')
def auth():
    return render_template('auth.html')

@routes.route('/handle_auth', methods=['POST'])
def handle_auth():
    if Auth.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first():
        session['username'] = request.form.get('username')
        return redirect('/dashboard')
    else:
        return abort(403)

@routes.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        if request.form.get('username'):
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
    return render_template('registo.html')

@routes.route('/logout')
def logout():
    if session:
        session.pop('username', None)
        session.clear()

    return redirect('/')

@routes.route('/clear_cookie')
def clear_cookie():
    data = request.get_json()
    new_value = data.get('new_value')

    session['errormsg'] = new_value
    return 'Error cookie new value {}'.format(session['errormsg'])

"""
@routes.route('/', defaults={'page':'index'}, methods=['GET', 'POST'])
@routes.route('/<page>', methods=['GET', 'POST'])
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404, "Não conseguimos localizar esta página. Código de erro: PAGE_NOT_FOUND")
"""