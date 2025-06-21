from flask import Flask
from flask_cors import CORS
from .utils.db import init_db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db(app)               # MongoDB setup
    register_routes(app)      # All API routes

    @app.route('/')
    def index():
        return app.send_static_file('index.html')  # Or render_template()

    return app
