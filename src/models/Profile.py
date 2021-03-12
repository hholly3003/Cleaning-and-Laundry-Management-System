from main import db
from models.Job import Job

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    jobs = db.relationship("Job", backref=db.backref("profiles", lazy="joined"), cascade="all, delete")

    def __repr__(self):
        return f"Profile: {self.firstname} {self.lastname}"