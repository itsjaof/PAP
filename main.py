from routes import routes, db, sess
from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='dist')

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:admin@localhost/pap'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SESSION_TYPE"] = 'sqlalchemy'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_SQLALCHEMY"] = db

db.init_app(app)
sess.init_app(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')