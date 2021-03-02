from main import ma
from models.JobType import JobType
from marshmallow.validate import ContainsOnly,Length,Range

class JobTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobType
    
    name = ma.String(required=True, validate=ContainsOnly(choices=["cleaning","laundry"]))
    price = ma.Integer(required=True, validate=Range(min=10))
    
job_type_schema = JobTypeSchema()
job_types_schema = JobTypeSchema(many=True)