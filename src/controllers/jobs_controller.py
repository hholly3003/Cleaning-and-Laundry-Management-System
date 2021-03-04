from main import db
from flask import Blueprint, jsonify, request, abort, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from forms import JobForm
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

@jobs.route("/job-view", methods=["GET","POST"])
@login_required
def index_view():
    jobs = Job.query.options(joinedload("profiles")).all()
    return render_template("index_job.html", jobs=jobs)

@jobs.route("/create-view", methods=["GET","POST"])
@login_required
def create_view():
    form = JobForm()
    if form.validate_on_submit():
        flash("Testing")
        profile = Profile.query.get(current_user.id)
        job_type = JobType.query.filter_by(name=form.job_requested.data).first()

        job = Job()
        job.cust_name = form.cust_name.data
        job.contact_num = form.contact_num.data
        job.job_requested = form.job_requested.data
        job.job_date = form.job_date.data
        print("*****************")
        job.job_time = form.job_time.data
        job.job_address = form.job_address.data
        job.job_notes = form.notes.data
        job.job_status = "Pending"
        profile.jobs.append(job)
        job_type.jobs.append(job)
        
        db.session.commit()
        print(job)

        flash("Your request is received!")
        return redirect(url_for("profiles.profile_view", id=profile.id))
    return render_template("create_job.html", form=form)

@jobs.route("/job-view/<int:id>", methods=["GET"])
@login_required
def job_view(id):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user")
        return redirect(url_for("auth.login_view"))   
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    job = Job.query.filter_by(id=id, profile_id=profile.id).first()

    if not job:
        flash("Unauthorised to access the job information")
        return redirect(url_for("jobs.index_view"))

    return render_template("job_page.html", job=job)

@jobs.route("/job-view/<int:id>", methods=["GET"])
@login_required
def delete_view(id):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user")
        return redirect(url_for("auth.login_view"))   
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    job = Job.query.filter_by(id=id, profile_id=profile.id).first()

    if not job:
        flash("Unauthorised to access the job information")
        return redirect(url_for("jobs.index_view"))

    return render_template("job_page.html", job=job)