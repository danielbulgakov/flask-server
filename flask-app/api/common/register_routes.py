from api.common.auth.routes import common_auth_bp

common_prefix='/api'

class CommonBPRegister:
    def __init__(self, app):
        self.app = app
        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(common_auth_bp, url_prefix=common_prefix)
