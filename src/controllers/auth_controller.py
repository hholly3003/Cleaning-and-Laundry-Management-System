from flask import Blueprint, abort, jsonify, request, abort
from flask_jwt_extended import create_access_token
from schemas.UserSchema import user_schema
from models.User import User
from main import db
from datetime import timedelta

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

@auth.route("/login", methods=["POST"])
def login():
    """
    Login for the users
    """

    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if user and user.check_password(user_fields["password"]):
        expiry = timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        return jsonify({"token": access_token})
    else:
        return abort(401, description="Unauthorized")

