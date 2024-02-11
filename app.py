from flask import Flask # Import da biblioteca flask para a criação do website.

# db = Aplicação da base de dados SQLAlchemy
# routes = blueprint com todas as rotas do website
# sess = Aplicação de sessões
from routes import db, routes, sess # Import do ficheiro routes.py, que contém as rotas do website, e a sua parte lógica

app = Flask(__name__, static_folder='dist') # Declaração da aplicação Flask com algumas configurações (Declaração da pasta static pois não é a padrão, __name__ para declarar onde está a aplicação flask (Neste caso, o mesmo ficheiro))

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost/pap" # Configuração da base de dados (flask_sqlalchemy)

# Configuração das sessões do site (flask_session)
app.config["SESSION_TYPE"] = 'sqlalchemy' # Configuração para que as sessões sejam armazenadas na base de dados (Tabela sessions).
app.config["SESSION_PERMANENT"] = False # Configuração para que as sessões não sejam permanentes.
app.config["SESSION_SQLALCHEMY"] = db # Configuração para indicar a aplicação SQlAlchemy.

# Inicialização dos "addons".
db.init_app(app)
sess.init_app(app)

app.register_blueprint(routes) # Registo de todas as rotas do website (Localizadas no ficheiro routes.py).

app.run(debug=True, host='0.0.0.0') # Inicialização do servidor com "debug" para obter mais informações para a resolução de problemas, host declarada para o website estar visível para toda a rede.