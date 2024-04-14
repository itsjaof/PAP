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
        return jsonify({"sucess" : "Autenticado com sucesso!"}), 200
    else:
        return abort(403)

@routes.route('/registo')
def registo():
    return render_template('registo.html')

@routes.route('/handle_register', methods=['POST'])
def handle_register():
    print('\n\n\nUtilizador: {}\nNome: {}\nEmail: {}\nPassword: {}\nRPassword: {}'.format(request.form.get('username'), request.form.get('name'), request.form.get('email'), request.form.get('password'), request.form.get('repeat-password')))

    if Auth.query.filter_by(email = request.form.get('email')).first():
        return jsonify({"error" : "Este email já foi registado."}), 500
        
    if Auth.query.filter_by(username = request.form.get('username')).first():
        return jsonify({"error" : "Este nome de utilizador já foi registado."}), 500
        
    if not request.form.get('password') == request.form.get('repeat-password'):
        return jsonify({"error" : "As palavras-passe devem ser iguais!"}), 500

    toCommit = Auth(username = request.form.get('username'), name = request.form.get('name'), password = request.form.get('password'), email = request.form.get('email'), type = 'USER')
    db.session.add(toCommit)
    db.session.commit()

    session['username'] = request.form.get('username')
    
    return jsonify({"sucess" : "Utilizador criado com sucesso!"}), 200

@routes.route('/logout')
def logout():
    if session:
        session.pop('username', None)
        session.clear()

    return redirect('/')

