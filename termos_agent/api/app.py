from flask import Flask

from termos_agent.api.routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
