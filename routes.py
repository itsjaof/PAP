# Implementação das bibliotecas necessárias assim como os seus módulos
from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Configuração para que este ficheiro possa criar rotas para o site
routes = Blueprint('routes', __name__, template_folder='templates')

# Inicialização das bibliotecas necessárias
db   = SQLAlchemy()
sess = Session()

"""
    AGENDA

    Campos:
    - `teacher_id`: ID do professor, é uma chave estrangeira que referencia 'auth.id'. Faz parte da chave primária composta.
    - `student_id`: ID do estudante, é uma chave estrangeira que referencia 'auth.id'. Faz parte da chave primária composta.
    - `date`: Data do agendamento, é parte da chave primária composta.
    - `type`: Tipo de agendamento, que pode ser um dos valores pré-definidos ('CÓDIGO', 'TEÓRICA', 'SIMULADOR', 'EXAME').

    Relações:
    - O relacionamento entre 'teacher_id' e 'student_id' é gerido com exclusão em cascata ('CASCADE'),
      o que significa que, se um professor ou aluno for removido, todos os compromissos associados também serão removidos.
"""

class Agenda(db.Model):
    teacher_id = db.Column(db.Integer, db.ForeignKey('auth.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('auth.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    date = db.Column(db.Date, primary_key=True, nullable=False)
    type = db.Column(db.Enum('CÓDIGO', 'TEÓRICA', 'SIMULADOR', 'EXAME'), nullable=False)

"""
    TESTEMUNHOS

    Campos:
    - `userid`: ID do utilizador que fez o testemunho, é uma chave estrangeira que referencia 'auth.id' com exclusão em cascata.
    - `testemunho`: O texto do testemunho, limitado a 250 caracteres.

    Relações:
    - Quando um utilizador é eliminado, todos o seu testemunho associado (caso exista) é removido devido à configuração de exclusão em cascata.
"""

class Testemunhos(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('auth.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    testemunho = db.Column(db.String(250), nullable=False)

"""
    AUTH

    Campos:
    - `id`: ID único do utilizador, é a chave primária.
    - `username`: Nome de utilizador, deve ser único e não pode ser nulo.
    - `password`: Palavra-passe do utilizador, não pode ser nula.
    - `email`: Endereço de email, deve ser único e não pode ser nulo.
    - `name`: Nome do utilizador, não pode ser nulo.
    - `picture`: Caso exista uma foto de perfil no servidor o valor é 1, caso contrário é 0.
    - `type`: Tipo de utilizador, que pode ser um dos valores pré-definidos ('USER', 'INSTRUTOR', 'ADMIN', 'STAFF').

    Relações:
    - `agenda_teacher`: Relaciona os agendamentos onde o utilizador é um professor.
    - `agenda_student`: Relaciona os agendamentos onde o utilizador é um estudante.
    - `testemunhos_user`: Relaciona o testemunho associado ao utilizador.
"""

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.Integer)
    type = db.Column(db.Enum('USER', 'STAFF', 'ADMIN'), nullable=False)

    agenda_teacher = db.Relationship('Agenda', cascade="all, delete-orphan", backref='teacher', lazy=True, foreign_keys=[Agenda.teacher_id])
    agenda_student = db.Relationship('Agenda', cascade="all, delete-orphan", backref='student', lazy=True, foreign_keys=[Agenda.student_id])
    testemunhos_user = db.Relationship('Testemunhos', cascade="all, delete-orphan", backref='user', lazy=True, foreign_keys=[Testemunhos.userid])

"""
    MESSAGES

    Campos:
    - `id`: ID único da mensagem, é a chave primária.
    - `name`: Nome do remetente, não pode ser nulo.
    - `email`: Endereço de email do remetente, não pode ser nulo.
    - `message`: Conteúdo da mensagem, não pode ser nulo.
"""

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String, nullable=False)

"""
    BEFORE REQUEST

    Esta função é chamada a cada pedido que for enviado para o servidor, tem como objetivo:
    1. Verificar se existe uma sessão ativa;
    2. Verificar se o utilizador tem uma foto de perfil acossiada;
    3. Caso tenha, guarda-a na variável `user_picture`, para poder ser utilizada.
"""

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

"""
    CONTEXT PROCESSOR

    Esta função tem como objetivo injetar a variável user_picture no código,
    para que possa ser utilizada quando necessário.
"""

@routes.context_processor
def inject_user_picture():
    return dict(user_picture=g.get('user_picture', None))

"""
    ERROR HANDLER

    Esta página é acionada quando existe algum erro no site, 
    e ela é substituida pelo documento original e mostra-nos o erro.
"""

@routes.errorhandler(Exception)
def error(error):
    return render_template('shared/error.html', error=error), 500

"""
    PÁGINA INICIAL

    Esta é a página inicial do site.
    A variável testemunhos é inicializada e guardada para que possa utilizar no HTML,
    com o objetivo de poder colocar os testemunhos que estão na base de dados no "swiper".
"""

@routes.route('/')
def index():
    testemunhos = Testemunhos.query.all()

    for content in testemunhos:
        content.name  = Auth.query.get(content.userid).name
        content.picture = Auth.query.get(content.userid).picture
        content.username = Auth.query.get(content.userid).username
    
    return render_template('index.html', testemunhos=testemunhos)

@routes.route('/send-message', methods=['POST'])
def send_email():
    new_message = Messages(name = request.form.get('name'), email = request.form.get('email'), message = request.form.get('message'))
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"sucess": "Mensagem enviada com sucesso!"}), 200

"""
    AUTENTICAÇÃO pt. 1

    Esta página está encarregada de mostrar o formulário de autentiação.
"""

@routes.route('/auth', endpoint='auth')
def auth():
    return render_template('auth.html')

"""
    AUTENTICAÇÃO pt. 2

    Esta página está encarregada de contactar a base de dados,
    cruzar os dados e verificar se estão corretos e autenticar o utilizador.
"""

@routes.route('/handle_auth', methods=['POST'])
def handle_auth():
    if Auth.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first():
        session['username'] = request.form.get('username')
        return jsonify({"sucess" : "Autenticado com sucesso!"}), 200
        
    return abort(403)

"""
    LOGOUT

    Esta página tem como objetivo terminar a sessão do utilizador,
    e redireciná-lo para a página inicial.
"""

@routes.route('/logout')
def logout():
    if session:
        session.pop('username', None)
        session.clear()

    return redirect('/')