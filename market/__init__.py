from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__,
            static_folder="templates/static/")  # static_folder - it is a connection to css files in current directory(templates/static)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '600fd5e0db220d4ec110321a'
api = Api(app)

# settings for SWAGGER
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
API_USER = '/static/swagger_example.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'market'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"  # if not log in , that this functions will redirect to 'login page'
login_manager.login_message_category = "info"
from market import routes, models
