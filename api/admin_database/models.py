from main import db

class Admin(db.Model):
    __tablename__ = 'admin'
    __bind_key__ = "admin_db"
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_salt = db.Column(db.String(255), nullable=False)

class Session(db.Model):
    __tablename__ = 'session'
    __bind_key__ = "admin_db"
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('admin.id'), nullable=False)
    expiration = db.Column(db.Integer, nullable=False)
    