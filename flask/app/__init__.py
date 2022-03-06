# from attr import validate
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../db/global_nat.db"
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
db = SQLAlchemy(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,  title='NAT LookUP API',
    version='1.0',
    description='API access to find NAT rules on SANE managed Firewalls.',
    doc='/doc', endpoint= "sas-automation-dr.1dc.com/api", default="NAT LookUP API")
app.register_blueprint(blueprint)
# assert url_for('api.doc') == '/api/doc/'

# api = api1.namespace('', description='NAT API operations')

from app import views
from app import views_api
