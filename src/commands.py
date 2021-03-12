from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

#Dropping all table
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    #Delete the alembic table
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

#Seeding sample data to the database table
@db_commands.cli.command("seed")
def seed_db():
    from models.User import User
    from models.Profile import Profile
    from models.JobType import JobType
    from main import bcrypt
    from faker import Faker

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

    print("Tables seeded")