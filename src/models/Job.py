from main import db
from datetime import datetime, date
from sqlalchemy.orm import backref

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(30), nullable=False)
    contact_num = db.Column(db.String(), nullable=False)
    job_requested = db.Column(db.String(), nullable=False)
    job_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    job_date = db.Column(db.Date, nullable=False, default=date.today())
    # job_time = db.Column(db.Time, default=datetime.now().time())
    job_address = db.Column(db.String(100), nullable=False)
    job_status = db.Column(db.String(), nullable=False, default="Pending")
    job_notes = db.Column(db.String(120))
    job_type_id = db.Column(db.Integer, db.ForeignKey("job_types.id"),nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)