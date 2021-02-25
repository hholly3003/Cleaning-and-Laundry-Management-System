from main import ma
from models.Profile import Profile
from marshmallow.validate import Length

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
    
    username = ma.String(required=True, validate=Length(min=1))
    firstname = ma.String(required=True, validate=Length(min=1))
    lastname = ma.String(required=True, validate=Length(min=1))
    user = ma.Nested(UserSchema)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)