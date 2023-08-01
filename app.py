from flask import Flask
from db import *
from geocaches import geocaches_api
from records import records_api
from user_analytics import *
from auth import auth_api
from flask_jwt_extended import JWTManager
import datetime
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

load_dotenv()

# Create a flask app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = 'True'
cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

# Register module blueprints
URL_PREFIX = "/api"
app.register_blueprint(geocaches_api, url_prefix=URL_PREFIX)
app.register_blueprint(auth_api, url_prefix=URL_PREFIX)
app.register_blueprint(records_api, url_prefix=URL_PREFIX)
app.register_blueprint(user_analytics_api, url_prefix=URL_PREFIX)

# Initialize JWTManager
jwt = JWTManager(app) 
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
