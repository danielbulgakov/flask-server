from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class DBStatus:
    OK = "OK"
    ERROR = "ERROR"

"""Base model class providing common database operations"""
class BaseModel:

    # Create a new record in the database
    def create(self):￼
            db.session.commit()
            return DBStatus.OK
        except Exception as e:
            print(f"Error creating record: {e}")
            return DBStatus.ERROR

    # Find a record by its ID
    @classmethod
    def find_by_id(cls, id):
        try:
            return cls.query.filter_by(id=id).first(), DBStatus.OK
        except Exception as e:
            print(f"Error finding record by ID: {e}")
            return None, DBStatus.ERROR

    # Update an existing record
    def update(self):
        try:
            db.session.commit()
            return DBStatus.OK
        except Exception as e:
            print(f"Error updating record: {e}")
            return DBStatus.ERROR

    # Delete an existing record
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return DBStatus.OK
        except Exception as e:
            print(f"Error deleting record: {e}")
            return DBStatus.ERROR

    # Return all records of this model
    @classmethod
    def return_all(cls):
        try:
            return cls.query.all(), DBStatus.OK
        except Exception as e:
            print(f"Error retrieving all records: {e}")
            return None, DBStatus.ERROR

"""Model representing users in the database."""
class users(db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    date_of_birth = db.Column(db.Date)

"""Model representing records in the database."""
class records(db.Model, BaseModel):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    reading_date = db.Column(db.Date, nullable=False)
    time_interval = db.Column(db.Interval, nullable=False)
    readings_data = db.Column(db.JSON)

"""Model representing authentication credentials in the database."""
class auth(db.Model, BaseModel):
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('users', backref=db.backref('auth', lazy=True))

    # Find an authentication record by login
    @classmethod
    def find_by_login(cls, login):
        try:
            return cls.query.filter_by(login=login).first(), DBStatus.OK
        except Exception as e:
            print(f"Error finding record by login: {e}")
            return None, DBStatus.ERROR

    # Find an authentication record by email
    @classmethod
    def find_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).first(), DBStatus.OK
        except Exception as e:
            print(f"Error finding record by email: {e}")
            return None, DBStatus.ERROR
