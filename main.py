from routes import routes, db, sess
from flask import Flask
import os # Biblioteca usada para esconder o nome de utilizador e palavra-passe nas variáveis de ambiente

app = Flask(__name__, template_folder='templates', static_folder='dist')

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:Joao_Pedro2006@192.168.1.119:3307/pap'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{}:{}@localhost:3307/pap'.format(os.environ.get("MYSQL_USERNAME"), os.environ.get("MYSQL_PASSWORD"))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SESSION_TYPE"] = 'sqlalchemy'
app.config["SESSION_SQLALCHEMY"] = db

db.init_app(app)
sess.init_app(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')