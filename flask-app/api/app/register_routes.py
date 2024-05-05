from api.common.auth.routes import app_auth_bp

common_prefix='/api/app'

class AppBPRegister:
    def __init__(self, app):
        self.app = app
        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(app_auth_bp, url_prefix=common_prefix)
