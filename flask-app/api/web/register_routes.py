from api.web.users.routes import web_users_bp

common_prefix='/api/web'

class WebBPRegister:
    def __init__(self, app):
        self.app = app
        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(web_users_bp, url_prefix=common_prefix)
