from flask import Blueprint, abort, jsonify, request
from schemas.UserSchema import user_schema
from models.User import User
from main import db

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def register():
    """
    User Registration

    POST request 
    """
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    #Check if the user has already existed in database
    if user:
        return abort(400, description="Email already registered")

    user = User()
    user.email = user_fields["email"]
    user.hash_password(user_fields["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))