from main import db
from flask import jsonify, request, Blueprint, abort, flash, render_template, redirect, url_for
from forms import ProfileForm
from models.User import User
from models.Profile import Profile
from schemas.ProfileSchema import profiles_schema, profile_schema
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

profiles = Blueprint("profiles", __name__, url_prefix="/profiles")

#ACCESS FOR ADMIN ONLY
@profiles.route("/", methods=["GET"])
@jwt_required()
def profile_index():
    profiles = Profile.query.all()
    profiles = Profile.query.options(joinedload("user")).all()
    return jsonify(profiles_schema.dump(profiles))

#RELATED USER ONLY
@profiles.route("/", methods=["POST"])
@jwt_required()
def profile_create():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    if user.profile != []:
        return abort(400, description="User already has a profile in the system")
    
    profile_fields = profile_schema.load(request.json)
    profile = Profile.query.filter_by(username=profile_fields["username"]).first()

    if profile:
        return abort(400, description="username is taken")
    
    new_profile = Profile()
    new_profile.username = profile_fields["username"]
    new_profile.firstname = profile_fields["firstname"]
    new_profile.lastname = profile_fields["lastname"]
    new_profile.user_id = user.id

    user.profile.append(new_profile)
    db.session.commit()

    return jsonify(profile_schema.dump(new_profile))

#ADMIN AND RELATED USER ONLY
@profiles.route("/<int:id>", methods=["GET"])
@jwt_required
def dashboard(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")
    
    profile = Profile.query.filter_by(id=id, user_id=user.id)

    if profile.count() != 1:
        return abort(404, description="Profile not found")

# #RELATED USER ONLY
# @profiles.route("/<int:id>", methods=["PUT","PATCH"])
# @jwt_required
# def profile_update(id):
#     user_id =get_jwt_identity()
#     user = User.query.get(user_id)

#     if not user:
#         return abort(401, description="Invalid User")
    
#     profile_fields = profile_schema.load(request.json)
#     profile = Profile.query.filter_by(id=id, user_id=user.id)

#     if not profile:
#         return abort(401, description="Unauthorised to update this profile")
    
#     profile.update(profile_fields)
#     db.session.commit()

#     return jsonify(profile_schema.dump(profile[0]))

# #RELATED USER ONLY
# @profiles.route("/<int:id>", methods=["DELETE"])
# @jwt_required
# def profile_delete(id):
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)

#     if not user:
#         return abort(401, description="Invalid user")
    
#     profile = Profile.query.filter_by(id=id, user_id=user.id).first()

#     if not profile:
#         return abort(401, description="Unathorised to delete this profile")
    
#     db.session.deletr(profile)
#     db.session.commit()

#     return jsonify(profile_schema.dump(profile))

@profiles.route("/create-view", methods=["GET","POST"])
@login_required
def create_view():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile.query.get(current_user.id)
        if profile:
            flash("You already have a profile")
            return redirect(url_for("profiles.profile_view", id=profile.id))
        profile = Profile()
        profile.username = current_user.email
        profile.firstname = form.firstname.data
        profile.lastname = form.lastname.data
        profile.user_id = current_user.id

        db.session.add(profile)
        db.session.commit()

        flash("Profile Created")
        return redirect(url_for("profiles.profile_view", id=profile.id))
    flash("Failed to create your profile.")
    return render_template("create_profile.html", form=form)

@profiles.route("/profile-view/<int:id>", methods=["GET"])
@login_required
def profile_view(id):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user")
        return redirect(url_for("auth.register_view"))
    
    profile = Profile.query.filter_by(id=id, user_id=user.id).first()

    if not profile:
        flash("Profile page can not be found")
        return redirect(url_for("profiles.create_view"))
    return render_template("profile_page.html", profile=profile)