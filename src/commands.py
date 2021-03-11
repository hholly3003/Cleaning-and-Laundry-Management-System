from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    #Delete the alembic table
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Profile import Profile
    from models.JobType import JobType
    from models.Job import Job
    from main import bcrypt
    from faker import Faker
    import random, datetime

    faker = Faker()
    users = []
    profiles = []
    services = [("cleaning", 50),("laundry",25)]
    job_types = []
    jobs = []

    #Create 5 users
    for i in range(5):
        user = User()
        user.email = f"test{i+1}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(users)
    #Create profile for the 5 users
    for i in range(5):
        profile = Profile()
        profile.username = users[i].email
        profile.firstname = faker.first_name()
        profile.lastname = faker.last_name()
        profile.user_id = users[i].id
        db.session.add(profile)
        profiles.append(profile)
    
    db.session.commit()

    #Create admin user
    user = User()
    user.email = "admin@test.com"
    user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
    user.is_admin = True
    db.session.add(user)
    db.session.commit()

    #Create admin profile
    profile = Profile()
    profile.username = "admin@test.com"
    profile.firstname = "admin"
    profile.lastname = "admin"
    profile.user_id = user.id
    db.session.add(profile)  
    db.session.commit()

    for i in range(2):
        job_type = JobType()
        job = services[i]
        job_type.name = job[0]
        job_type.price = job[1]
        db.session.add(job_type)
        job_types.append(job_type)
    
    db.session.commit()

    for i in range(5):
        job = Job()
        job_type = random.choice(job_types)
        job.cust_name = faker.name()
        job.contact_num = faker.phone_number()
        job.job_requested = job_type.name
        job.job_date = faker.future_date()
        job.job_time = faker.time_object()
        job.job_address = faker.address()
        job.job_status = "Pending"
        job.notes = ""
        job.profile_id = profiles[i].id
        job.job_type_id = job_type.id
        db.session.add(job)
        jobs.append(job)

    db.session.commit()
