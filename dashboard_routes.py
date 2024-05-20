from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, url_for, current_app, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from routes import db, sess, Auth, Messages, Agenda
import os

dashboard_routes = Blueprint('dashboard', __name__)

def check_session():
    if not session.get('username'):
        raise abort(500, 'AUTH_COOKIE_NOT_FOUND')

@dashboard_routes.before_request
def get_user_picture():
    if session:
        query = db.session.execute(
            db.select(Auth).filter_by(username=session.get('username'))
        ).scalar_one_or_none()
        
        if query:
            g.user_picture = query.picture
    else:
        g.user_picture = None

@dashboard_routes.context_processor
def inject_user_picture():
    return dict(user_picture=g.get('user_picture', None))

@dashboard_routes.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect('/auth')
    
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    current_time = datetime.now().hour

    return render_template('/dashboard/dashboard.html', user=user, current_time=current_time)

@dashboard_routes.route('/dashboard/messages')
def messages():
    check_session()
    
    messages = Messages.query.all()
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))

    if user.type == 'USER':
        return redirect('/dashboard')

    return render_template('dashboard/messages.html', messages=messages, user=user)

@dashboard_routes.route('/dashboard/agenda', methods=['GET'])
def submit_agenda():
    check_session()

    students = Auth.query.filter_by(type="USER")
    agenda = Agenda.query.all()
    user_id = db.one_or_404(db.select(Auth).filter_by(username=session['username'])).id
    user_type = Auth.query.filter_by(id = user_id).first().type

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    for content in agenda:
        teacher_name = Auth.query.get(content.teacher_id).name
        teacher_username = Auth.query.get(content.teacher_id).username
        teacher_email= Auth.query.get(content.teacher_id).email
        student_name = Auth.query.get(content.student_id).name
        
        content.teacher_name = teacher_name
        content.teacher_username = teacher_username
        content.teacher_email = teacher_email
        content.student_name = student_name

    return render_template('dashboard/agenda.html', user=user, students=students, user_id=user_id, agenda=agenda, user_type=user_type)

@dashboard_routes.route('/submit-agenda', methods=['POST'])
def agenda():
    check_session()

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

@dashboard_routes.route('/dashboard/perfil')
def profile():
    check_session()

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    return render_template('dashboard/profile.html', user=user)

@dashboard_routes.route('/update-profile-picture', methods=['POST'])
def update_profile_picture():
    check_session()

    if 'profile-picture' not in request.files:
        return jsonify({'error': 'O ficheiro enviado não é válido.'}), 500
    
    file = request.files['profile-picture']
    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], session['username'] + '.png'))
    user.picture = 1
    db.session.commit()

    return jsonify({"sucesso": "foto de perfil atualizada com sucesso."}), 200

@dashboard_routes.route('/dashboard/users')
def users():
    check_session()

    users = Auth.query.all()

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    return render_template('dashboard/utilizadores.html', users=users, user=user)

@dashboard_routes.route('/dashboard/marcar')
def marcar():
    check_session()

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    return render_template('dashboard/marcar.html', user=user)

@dashboard_routes.route('/search-message-email', methods=['POST'])
def search_message_email():
    ...