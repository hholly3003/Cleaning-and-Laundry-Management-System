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

@jobs.route("/", methods=["GET"])
@jwt_required()
def job_index():
    user_id = get_jwt_identity()
    user =  User.query.get(user_id)
    
    if user.is_admin == True:
        jobs = Job.query.options(joinedload("profiles")).all()
    else:
        profile = Profile.query.filter_by(user_id=user.id).first()
        jobs = Job.query.filter_by(profile_id=profile.id)
    return jsonify(jobs_schema.dump(jobs))

@jobs.route("/", methods=["POST"])
@jwt_required()
def job_create():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")
    
    profile = Profile.query.filter_by(user_id=user.id).first()

    job_fields = job_schema.load(request.json)

    job_type = JobType.query.filter_by(name=job_fields["job_requested"]).first()

    if not job_type:
        return abort(404, description="Sorry, we do not have that service")

    new_job = Job()
    new_job.cust_name = job_fields["cust_name"]
    new_job.contact_num = job_fields["contact_num"]
    new_job.job_requested = job_fields["job_requested"]
    new_job.job_date = job_fields["job_date"]
    new_job.job_time = job_fields["job_time"]
    new_job.job_address = job_fields["job_address"]
    new_job.job_status = job_fields["job_status"]
    new_job.job_notes = job_fields["job_notes"]
    new_job.profile_id = profile.id
    job_type.jobs.append(new_job)
    
    db.session.commit()
    
    return jsonify(job_schema.dump(new_job)), 201

@jobs.route("/<int:id>", methods=["GET"])
@jwt_required()
def job(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return abort(401, description="Invalid user")
    
    profile = Profile.query.filter_by(user_id=user.id).first()

    if user.is_admin == False:
        if profile.jobs == []:
            return abort(400, description="There is no job(s) in your account")

        job = Job.query.filter_by(id=id, profile_id=profile.id)

        if job.count() != 1:
            return abort(401, description="Unauthorised to access this job information")
    else:
        job = Job.query.filter_by(id=id)
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

    if user.is_admin == True:
        job = Job.query.filter_by(id=id)
    else:
        job = Job.query.filter_by(id=id, profile_id=profile.id)
        if job.count() != 1:
            return abort(401, description="Unauthorised to update this job details")
    
    job.update(job_fields)
    db.session.commit()

    return jsonify(job_schema.dump(job[0]))

@jobs.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def job_delete(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    if user.is_admin == True:
        job = Job.query.filter_by(id=id).first()
        if not job:
            return abort(404, description="Job is not existed in the system")
        db.session.delete(job)
        db.session.commit()
    else:
        return abort(401, description="Unauthorised user")
    return jsonify(job_schema.dump(job))

@jobs.route("/job-view", methods=["GET","POST"])
@login_required
def index_view():
    user = User.query.get(current_user.id)
    profile = Profile.query.filter_by(user_id=user.id).first()
    jobs = Job.query.filter_by(profile_id=profile.id)

    return render_template("index_job.html", jobs=jobs)

@jobs.route("/job-view/admin", methods=["GET","POST"])
@login_required
def admin_view():
    user = User.query.get(current_user.id)
    if user.is_admin == True:
        jobs = Job.query.options(joinedload("profiles")).all()
    else:
        flash("You need an admin access", category="info")
        return redirect(url_for("jobs.index_view"))
    return render_template("index_job.html", jobs=jobs)

@jobs.route("/create-view", methods=["GET","POST"])
@login_required
def create_view():
    form = JobForm()
    
    if form.validate_on_submit():
        user = User.query.get(current_user.id)

        profile = Profile.query.filter_by(user_id=user.id).first()
        job_type = JobType.query.filter_by(id=form.job_requested.data).first()
        print(job_type.jobs)

        job = Job()
        job.cust_name = form.cust_name.data
        job.contact_num = form.contact_num.data
        job.job_requested = job_type.name
        job.job_date = form.job_date.data
        job.job_time = form.job_time.data
        
        keys = list(form.job_address.data)
        address = ", "
        values =[]
        for key in keys:
            value = form.job_address.data.get(key)
            values.append(str(value))
        job.job_address = address.join(values)

        job.job_notes = form.notes.data
        job.job_status = "Pending"
        profile.jobs.append(job)
        job_type.jobs.append(job)
        print(job_type.jobs)
        db.session.commit()

        flash("Your request is received!", category="success")
        return redirect(url_for("jobs.job_view", id=job.id))
    return render_template("create_job.html", form=form)

@jobs.route("/job-view/<int:id>", methods=["GET"])
@login_required
def job_view(id):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user", category="warnings")
        return redirect(url_for("auth.login_view"))   
    
    profile = Profile.query.filter_by(user_id=user.id).first()
    print(profile.jobs)
    if user.is_admin == True:
        job = Job.query.filter_by(id=id).first()
        print(job.id, job.cust_name)
    else:
        job = Job.query.filter_by(id=id, profile_id=profile.id).first()
        print(job.id, job.cust_name)

    if not job:
        flash("Unauthorised to access the job information", category="info")
        return redirect(url_for("jobs.index_view"))

    return render_template("job_page.html", job=job, profile=profile)

@jobs.route("/update-view/<int:id>/<string:status>", methods=["GET","POST"])
@login_required
def update_view(id, status):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user")
        return redirect(url_for("auth.login_view"))   
    
    profile = Profile.query.filter_by(user_id=user.id).first()

    if user.is_admin==True or status == "Cancelled":
        job = Job.query.filter_by(id=id)
        update_status = {"job_status":status}
        job.update(update_status)
        db.session.commit()
        flash(f"The job is {status}", category="info")
        return redirect(url_for("jobs.job_view", id=job.first().id))
    else:
        job = Job.query.filter_by(id=id, profile_id=profile.id)

    if job.count() != 1:
        flash("Unauthoried to update this job details", category="info")
        return redirect(url_for("jobs.index_view"))
    job_detail = job.first()

    # Prefill the form with the existing data
    form = JobForm(obj=job_detail)
    job_address = job_detail.job_address.split(", ")
    form.job_address.street_name.data = job_address[0]
    form.job_address.suburb.data = job_address[1]
    form.job_address.state.data = job_address[2]
    form.job_address.postcode.data = job_address[3]

    if form.validate_on_submit():
        # Getting new value
        job_type = JobType.query.filter_by(id=form.job_requested.data).first()

        keys = list(form.job_address.data)
        address = ", "
        values =[]
        for key in keys:
            value = form.job_address.data.get(key)
            values.append(str(value))

        job_fields = {
            "cust_name":form.cust_name.data,
            "contact_num":form.contact_num.data,
            "job_requested":job_type.name,
            "job_date":form.job_date.data,
            "job_time":form.job_time.data,
            "job_address":address.join(values),
            "job_notes":form.notes.data,
            "job_status":status,
            "profile_id":profile.id,
            "job_type_id":job_type.id
        }
        print(job)
        job.update(job_fields)
        print(job)
        db.session.commit()

        flash("Your data is updated!", category="success")
        return redirect(url_for("jobs.job_view", id=job_detail.id))
    return render_template("update_job.html", form=form, job=job_detail)

#ADMIN ONLY ACCESS
@jobs.route("/delete-view/<int:id>", methods=["GET","POST"])
@login_required
def delete_view(id):
    user_id = current_user.id
    user = User.query.get(user_id)

    if not user:
        flash("Invalid user")
        return redirect(url_for("auth.login_view"))   
    
    if user.is_admin == True:
        job = job = Job.query.filter_by(id=id).first()
        if not job:
            flash("The job is not existed in the system", category="info")
            return redirect(url_for("jobs.index_view"))

        db.session.delete(job)
        db.session.commit()
        flash("Job is deleted", category="danger")
        return redirect(url_for("jobs.index_view"))
    else:
        flash("Unauthorised to cancel this job", category="info")
        return redirect(url_for("jobs.index_view"))
        db.session.delete(job)
        db.session.commit()
        flash("Job is deleted", category="danger")
        return redirect(url_for("jobs.index_view"))
    return render_template("job_page.html", job=job)