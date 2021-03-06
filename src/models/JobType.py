from main import db

class JobType(db.Model):
    __tablename__="job_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    jobs = db.relationship("Job", backref=db.backref("job_type"))

    def __repr__(self):
        return f"JobType: {self.id} {self.name}"