from main import db
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.User import User
from models.Job import Job
from models.Profile import Profile
from models.JobType import JobType
from schemas.JobSchema import jobs_schema, job_schema
from sqlalchemy.orm import joinedload

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")

#ADMIN ONLY
@jobs.route("/", methods=["GET"])
@jwt_required()
def job_index():
    jobs = Job.query.options(joinedload("profiles")).all()
    return jsonify(jobs_schema.dump(jobs))

#RELATED USER ONLY
@jobs.route("/", methods=["POST"])
@jwt_required()
def job_create():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    print(profile.__dict__)

    job_fields = job_schema.load(request.json)

    job_type = JobType.query.filter_by(name=job_fields["job_requested"]).first()

    if not job_type:
        return abort(400, description="Sorry, we do not have that service")

    new_job = Job()
    new_job.cust_name = job_fields["cust_name"]
    new_job.contact_num = job_fields["contact_num"]
    new_job.job_requested = job_fields["job_requested"]
    new_job.job_date = job_fields["job_date"]
    # new_job.job_time = job_fields["job_time"]
    new_job.job_address = job_fields["job_address"]
    new_job.job_status = job_fields["job_status"]
    new_job.job_notes = job_fields["job_notes"]
    new_job.profile_id = profile.id
    job_type.jobs.append(new_job)
    
    db.session.commit()

    return jsonify(job_schema.dump(new_job))

#ADMIN AND RELATED USER ONLY
@jobs.route("/<int:id>", methods=["GET"])
@jwt_required()
def job(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return abort(401, description="Invalid user")
    
    profile = Profile.query.filter_by(user_id=user.id).first()

    if profile.jobs == []:
        return abort(400, description="There is no job(s) in your account")

    job = Job.query.filter_by(id=id, profile_id=profile.id)

    if job.count() != 1:
        return abort(401, description="Unauthorised to access this job information")
    return jsonify(job_schema.dump(job[0]))

#RELATED USER ONLY
@jobs.route("/<int:id>", methods=["PUT","PATCH"])
@jwt_required()
def job_update(id):
    user_id =get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid User")
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    job_fields = job_schema.load(request.json)

    job = Job.query.filter_by(id=id, profile_id=profile.id)
    if job.count() != 1:
        return abort(401, description="Unauthorised to update this job details")
    
    job.update(job_fields)
    db.session.commit()

    return jsonify(job_schema.dump(job[0]))

#RELATED USER ONLY
@jobs.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def job_delete(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    profile = Profile.query.filter_by(user_id=user.id).first()
    
    job = Job.query.filter_by(id=id, profile_id=profile.id).first()

    if not job:
        return abort(401, description="Unathorised to delete this job")
    
    db.session.delete(job)
    db.session.commit()

    return jsonify(job_schema.dump(job))

# @profiles.route("/create-view", methods=["GET","POST"])
# @login_required
# def create_view():
#     form = ProfileForm()
#     if form.validate_on_submit():
#         profile = Profile.query.get(current_user.id)
#         if profile:
#             flash("You already have a profile")
#             return redirect(url_for("profiles.profile_view", id=profile.id))
#         else:
#             profile = Profile()
#             profile.username = current_user.email
#             profile.firstname = form.firstname.data
#             profile.lastname = form.lastname.data

#             user.profile.append(profile)
#             db.session.commit()

#             flash("Profile Created")
#             return redirect(url_for("profiles.profile_view", id=profile.id))
#         flash("Failed to create your profile.")
#     return render_template("create_profile.html", form=form)

# @profiles.route("/profile-view/<int:id>", methods=["GET"])
# @login_required
# def profile_view(id):
#     user_id = current_user.id
#     user = User.query.get(user_id)

#     if not user:
#         flash("Invalid user")
#         return redirect(url_for("auth.login_view"))
    
#     if user.profile == []:
#         flash("Profile page can not be found")
#         return redirect(url_for("profiles.create_view"))    
    
#     profile = Profile.query.filter_by(id=id, user_id=user.id).first()

#     if not profile:
#         flash("Unauthorised to access the requested profile")
#         return redirect(url_for("profiles.profile_view", id=user.id))

#     return render_template("profile_page.html", profile=profile)