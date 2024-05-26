from flask import Flask # Implementação da biblioteca Flask para a inicialização da aplicação
from waitress import serve
from datetime import timedelta
import os

# db = Aplicação da base de dados SQLAlchemy
# routes = blueprint com todas as rotas do website
# sess = Aplicação de sessões
from routes import routes, db, sess, error # Import do ficheiro routes.py, que contém as rotas do website, e a sua parte lógica
from dashboard_routes import dashboard_routes

# Declaração da aplicação Flask com algumas configurações (Declaração da pasta static pois não é a padrão, __name__ para declarar onde está a aplicação flask (Neste caso, o mesmo ficheiro))
app = Flask(__name__, template_folder='templates', static_folder='dist')

# Configuração da conexão à base de dados (flask_sqlalchemy)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:Joao_Pedro2006@192.168.1.119:3307/pap'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Configuração das sessões do site (flask_session)
app.config['SECRET_KEY'] = 'N52~U6O,,Fo^/rSuJby2gxscBFyxR$'
app.config["SESSION_TYPE"] = 'sqlalchemy'
app.config["SESSION_SQLALCHEMY"] = db
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

app.config["UPLOAD_FOLDER"] = './dist/uploads'

# Inicialização dos componentes necessários
db.init_app(app)
sess.init_app(app)

# Registo das rotas do website
app.register_blueprint(routes)
app.register_blueprint(dashboard_routes)
app.register_error_handler(Exception, error)

# Inicialização do servidor com "debug" para obter mais informações para a resolução de problemas, host declarada para o website estar visível para toda a rede.
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # serve(app, host='0.0.0.0', port=3000)
    app.run(debug=True, host='0.0.0.0', port=3000)