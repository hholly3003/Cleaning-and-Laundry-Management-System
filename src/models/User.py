from main import db, bcrypt
from sqlalchemy.orm import backref
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    # profile = db.relationship("Profile", backref="user")

    def hash_password(self, password):
        """Hashed the password"""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        """Check the password hash"""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User: {self.email}"