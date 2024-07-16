from main import db

class Admin(db.Model):
    __tablename__ = 'admin'
    __bind_key__ = "admin_db"
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

