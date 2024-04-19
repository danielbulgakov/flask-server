from flask import Flask, render_template
from api.common.register_routes import register_common_blueprints
from database.db import init_db

app = Flask(__name__)

# Register blueprints
def register_blueprints(app):
    register_common_blueprints(app)

# Init dependency modules
register_blueprints(app)

# Init db
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://root:root@postgres:5432/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

# DONT forget to remove
@app.route('/')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
