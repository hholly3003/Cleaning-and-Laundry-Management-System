from main import ma
from models.Job import Job
from schemas.JobTypeSchema import JobTypeSchema
from schemas.ProfileSchema import ProfileSchema
from marshmallow.validate import Length, OneOf

class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
    
    cust_name = ma.String(required=True, validate=Length(min=1))
    contact_num = ma.String(required=True, validate=Length(min=1))
    job_requested = ma.String(required=True, validate=OneOf(choices=["cleaning","laundry"]))
    job_created = ma.DateTime(required=True)
    job_date = ma.Date(required=True)
    # job_time = ma.Time()
    job_address = ma.String(required=True, validate=Length(min=10))
    notes = ma.String()
    job_type = ma.Nested(JobTypeSchema)
    profile = ma.Nested(ProfileSchema)


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)