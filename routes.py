from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime

routes = Blueprint('routes', __name__, template_folder='templates')

db   = SQLAlchemy()
sess = Session()

class Agenda(db.Model):
    teacher_id = db.Column(db.Integer, db.ForeignKey('auth.id'), primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('auth.id'), primary_key=True, nullable=False)
    date = db.Column(db.Date, primary_key=True, nullable=False)
    type = db.Column(db.Enum('CÓDIGO', 'TEÓRICA', 'SIMULADOR', 'EXAME'), nullable=False)

class Testemunhos(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('auth.id'), primary_key=True, nullable=False)
    testemunho = db.Column(db.String(250), nullable=False)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.Integer)
    type = db.Column(db.Enum('USER', 'ADMIN', 'STAFF'), nullable=False)

    agenda_teacher = db.Relationship('Agenda', backref='teacher', lazy=True, foreign_keys=[Agenda.teacher_id])
    agenda_student = db.Relationship('Agenda', backref='student', lazy=True, foreign_keys=[Agenda.student_id])
    testemunhos_user = db.Relationship('Testemunhos', backref='user', lazy=True, foreign_keys=[Testemunhos.userid])

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String, nullable=False)

@routes.before_request
def get_user_picture():
    if session:
        query = db.session.execute(
            db.select(Auth).filter_by(username=session.get('username'))
        ).scalar_one_or_none()
        
        if query:
            g.user_picture = query.picture
    else:
        g.user_picture = None

@routes.context_processor
def inject_user_picture():
    return dict(user_picture=g.get('user_picture', None))

@routes.errorhandler(Exception) # Website error handler
def error(error):
    return render_template('shared/error.html', error=error), 500

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_message = Messages(name = request.form.get('name'), email = request.form.get('email'), message = request.form.get('message'))
        db.session.add(new_message)
        db.session.commit()
    
    testemunhos = Testemunhos.query.all()

    for content in testemunhos:
        name = Auth.query.get(content.userid).name

        content.name = name
    
    return render_template('index.html', testemunhos=testemunhos)

@routes.route('/auth', endpoint='auth')
def auth():
    return render_template('auth.html')

@routes.route('/handle_auth', methods=['POST'])
def handle_auth():
    if Auth.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first():
        session['username'] = request.form.get('username')
        return jsonify({"sucess" : "Autenticado com sucesso!"}), 200
        
    return abort(403)

@routes.route('/logout')
def logout():
    if session:
        session.pop('username', None)
        session.clear()

    return redirect('/')

"""

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

"""

