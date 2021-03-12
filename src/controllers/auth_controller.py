from flask import Blueprint, abort, jsonify, request, abort, redirect,url_for, flash, render_template
from flask_jwt_extended import create_access_token
from flask_login import current_user, login_user, logout_user, login_required
from schemas.UserSchema import user_schema, users_schema
from models.User import User
from main import db, login_manager
from forms import LoginForm, RegisterForm
from datetime import timedelta

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def register():
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

    return jsonify(user_schema.dump(user)),201

@auth.route("/login", methods=["POST"])
def login():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if user and user.check_password(user_fields["password"]):
        expiry = timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        return jsonify({"token": access_token})
    else:
        return abort(401, description="Unauthorized")

# get all the user
@auth.route("/users", methods=["GET"])
def user_index():
    user = User.query.all()
    return jsonify(users_schema.dump(user))

@login_manager.user_loader
def load_user(user_id):
    """ Check if user is logged in on every page load """
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """ Redirect unauthorized users to Login page """
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login_view"))

@auth.route("/register-view", methods=["GET", "POST"])
def register_view():
    """
    User registration page

    GET requests render registration page
    POST requests validate and user creation
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user has already existed in the database
        if user:
            flash("Email already registered.")
        
        # New user creation
        user = User()
        user.email = form.email.data
        user.hash_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("profiles.create_view"))
    return render_template("register.html", form=form)   

@auth.route("/login-view", methods=["GET", "POST"])
def login_view():
    """
    Login page for registered user

    GET requests render login page
    POST requests validate and redirect user to dashboard
    """

    #Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("profiles.profile_view",id=current_user.id))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #Check if the password matched
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for(f"profiles.profile_view", id=current_user.id))
        flash("Invalid email and password.")
        return redirect(url_for("auth.login_view"))
    return render_template("login.html", form=form)

#logged the authenticated user out from the system
@auth.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_view"))