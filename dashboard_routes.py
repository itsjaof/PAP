from flask import Blueprint, render_template, request, session, redirect, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from routes import db, sess, Auth, Messages, Agenda

dashboard_routes = Blueprint('dashboard', __name__)

def check_session():
    if not session.get('username'):
        raise abort(500, 'AUTH_COOKIE_NOT_FOUND')

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
    return render_template('dashboard/messages.html', messages=messages, user=user)

@dashboard_routes.route('/dashboard/agenda', methods=['GET'])
def submit_agenda():
    check_session()

    students = Auth.query.filter_by(type = "USER")

    user = db.one_or_404(db.select(Auth).filter_by(username=session['username']))
    return render_template('dashboard/agenda.html', user=user, students=students)

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