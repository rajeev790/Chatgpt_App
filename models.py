from app import db

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120))
