from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, url_for, current_app, g
from datetime import datetime
from routes import db, Auth, Messages, Agenda, Testemunhos
import os

dashboard_routes = Blueprint('dashboard', __name__)

"""
    VERIFICAR SESSÃO
    
    Esta função tem como objetivo verificar se existe uma sessão ativa,
    caso não exista, retorna o erro 403 (PROÍBIDO)
"""

def check_session():
    if not session.get('username'):
        return redirect(url_for('routes.auth'))
    
    return None

"""
    VERIFICAR SESSÃO POR PERMISSÃO
    
    Esta função tem como objetivo verificar se a sessão ativa pertence a um grupo de utilizadores,
    caso não pertença, retorna o erro 403 (PROÍBIDO)
"""

def check_session_type(TYPE):
    if not g.user_type == TYPE:
        raise abort(403)

"""
    BEFORE REQUEST

    Esta função é chamada a cada pedido que for enviado para o servidor, tem como objetivo:
    1. Verificar se existe uma sessão ativa;
    2. Verificar se o utilizador tem uma foto de perfil acossiada,
    caso tenha, guarda-a na variável `user_picture`, para poder ser utilizada;
    3. Guardar o grupo de permissões do utilizado na variável `user_type`;
    4. Guardar o nome do utilizado na variável `user_name`.
"""

@dashboard_routes.before_request
def get_user_picture():
    if session:
        query = db.session.execute(
            db.select(Auth).filter_by(username=session.get('username'))
        ).scalar_one_or_none()
        
        if query:
            g.user_type = query.type
            g.user_picture = query.picture
            g.user_name = query.name
    else:
        g.user_type = None
        g.user_picture = None
        g.user_name = None

"""
    CONTEXT PROCESSOR

    Esta função tem como objetivo injetar a variável user_picture e user_name no código,
    para que possa ser utilizada quando necessário.
"""

@dashboard_routes.context_processor
def inject_user_picture():
    return dict(user_picture=g.get('user_picture', None), 
                user_name=g.get('user_name', None))

"""
    PÁGINA PRINCIPAL
"""

@dashboard_routes.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect('/auth')
    
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    current_time = datetime.now().hour

    return render_template('/dashboard/dashboard.html', user=user, current_time=current_time)

"""
    MENSAGENS
"""

@dashboard_routes.route('/dashboard/messages')
def messages():
    if check_session():
        return check_session()
    
    messages = Messages.query.all()
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))

    if user.type == 'USER':
        return redirect('/dashboard')

    return render_template('dashboard/messages.html', messages=messages, user=user)

@dashboard_routes.route('/delete-message/<int:user_id>', methods=['POST'])
def delete_message(user_id):
    if check_session():
        return check_session()
    
    message = Messages.query.filter_by(id=user_id).first()

    if message:
        db.session.delete(message)
        db.session.commit
        return jsonify({"sucess" : "Mensagem eliminada com sucesso!"}), 200

    return jsonify({"error": "Ocorreu um erro ao eliminar a mensagem."}), 500

"""
    AGENDA
"""

@dashboard_routes.route('/dashboard/agenda', methods=['GET'])
def submit_agenda():
    if check_session():
        return check_session()

    students = Auth.query.filter_by(type="USER")
    agenda = Agenda.query.all()
    user_id = db.one_or_404(db.select(Auth).filter_by(username=session['username'])).id
    user_type = Auth.query.filter_by(id = user_id).first().type

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    for content in agenda:
        content.teacher_name = Auth.query.get(content.teacher_id).name
        content.teacher_username = Auth.query.get(content.teacher_id).username
        content.id = Auth.query.get(content.teacher_id).id
        content.teacher_email= Auth.query.get(content.teacher_id).email
        content.student_name = Auth.query.get(content.student_id).name

    return render_template('dashboard/agenda.html', user=user, students=students, user_id=user_id, agenda=agenda, user_type=user_type)

@dashboard_routes.route('/submit-agenda', methods=['POST'])
def agenda():
    if check_session():
        return check_session()

    teacher = db.one_or_404(db.select(Auth).filter_by(username = session['username'])).id
    student = db.one_or_404(db.select(Auth).filter_by(username = request.form.get('student'))).id

    print(teacher)
    print(student)

    toCommit = Agenda(
        teacher_id = teacher, 
        student_id = student, 
        date = request.form.get('date'), 
        type = request.form.get('type')
    )

    db.session.add(toCommit)
    db.session.commit()

    return jsonify({"sucess" : "Agendamento criado com sucesso!"}), 200

@dashboard_routes.route('/delete-schedule', methods=['POST'])
def delete_agenda():
    if check_session():
        return check_session()

    teacher_id = request.form.get('teacher_id')
    student_id = request.form.get('student_id')
    date = request.form.get('date')
    type = request.form.get('type')

    schedule = Agenda.query.filter_by(
        teacher_id=teacher_id,
        student_id=student_id,
        date=date,
        type=type
    ).first()

    if schedule:
        db.session.delete(schedule)
        db.session.commit
        return jsonify({"sucess" : "Agendamento eliminado com sucesso!"}), 200

    return jsonify({"error" : "Ocorreu um erro ao eliminar o agendamento."}), 500

"""
    UTILIZADORES
"""

@dashboard_routes.route('/dashboard/users')
def users():
    check_session_type('ADMIN')

    users = Auth.query.all()

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    return render_template('dashboard/utilizadores.html', users=users, user=user)

@dashboard_routes.route('/add-user', methods=['POST'])
def adduser():
    check_session_type('ADMIN')
    
    toCommit = Auth(
        username = request.form.get('username'),
        name = request.form.get('name'),
        email = request.form.get('email'),
        password = request.form.get('password'),
        type = request.form.get('type'),
        picture = 0
    )

    db.session.add(toCommit)
    db.session.commit()

    return jsonify({"sucess" : "Utilizador criado com sucesso!"}), 200

@dashboard_routes.route('/update-user/<int:user_id>', methods=['POST'])
def update(user_id):
    check_session_type('ADMIN')

    to_update = Auth.query.filter_by(id=user_id).first()

    if not to_update:
        return jsonify({"error": "Utilizador não encontrado"}), 404
    
    fields = ['username', 'password', 'name', 'type', 'email']

    for field in fields:
        if request.form.get(field):
            setattr(to_update, field, request.form.get(field))
    
    db.session.commit()

    return jsonify({"sucess": "Utilizador atualizado com sucesso"}), 200

@dashboard_routes.route('/remove/<int:user_id>', methods=['POST'])
def remove(user_id):
    check_session_type('ADMIN')

    user = db.one_or_404(db.select(Auth).filter_by(id=user_id))
    db.session.delete(user)
    db.session.commit()

    return jsonify({"sucess": "Utilizador removido com sucesso"}), 200

"""
    PERFIL
"""

@dashboard_routes.route('/dashboard/perfil')
def profile():
    if check_session():
        return check_session()

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    testemunho = db.session.execute(db.select(Testemunhos).filter_by(userid=user.id)).scalar_one_or_none()

    return render_template('dashboard/profile.html', user=user, testemunho=testemunho)

@dashboard_routes.route('/update-profile-picture', methods=['POST'])
def update_profile_picture():
    if check_session():
        return check_session()

    if 'profile-picture' not in request.files:
        return jsonify({'error': 'O ficheiro enviado não é válido.'}), 500
    
    file = request.files['profile-picture']
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], session['username'] + '.png'))
    user.picture = 1
    db.session.commit()

    return jsonify({"sucesso": "foto de perfil atualizada com sucesso."}), 200

@dashboard_routes.route('/send-testemunho', methods=['POST'])
def send_testemunho():
    toCommit = Testemunhos()
    toCommit.userid = db.one_or_404(db.select(Auth).filter_by(username=session['username'])).id
    toCommit.testemunho = request.form.get("testemunho")

    db.session.add(toCommit)
    db.session.commit()
    
    return jsonify({"sucess": "Testemunho enviado com sucesso!"}), 200

"""
PÁGINA DE TEMPLATE

@dashboard_routes.route('/temp')
def temp():
    check_session()
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))

    return render_template('temp.html', user=user)
"""