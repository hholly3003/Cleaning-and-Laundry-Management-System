# Cleaning and Laundry Management
---
### Help and Installation Guide
---
**System Requirement**: Please ensure that Python3 is installed on your machine
#### Project and Environment Setup
- Clone the repository to your local machine
- Create virtual environment and activate
- Install all dependencies
- Run the application
#### Database Setup
- Install PostgreSQL on your host
- Log into PostgreSQL as postgres user
- Create database for the management system
- Set up .env folder
---
### About the Project
  The purpose of the **Cleaning and Laundry Management System** website is to accept a laundry order from the customer and manage the order, such as organising the schedule delivery, sending confirmation of order, and accepting payments. The benefits are getting all customer order recorded automatically, well organised, and never miss out or lost any order.

  In today's condition of COVID-19 pandemic where we need to keep distance to each other to minimalise contact, all business is required to use Internet technology to reach out to their customer. This includes businesses who provide services of cleaning and laundry. At the moment, people acquire their services via call, submit an enquire via their static website and need to wait for the admin to send a reply. Then, the admin recorded the job order manually. The process is semi-manual and often the admin forget to reply to the customer enquiry or miss the call. This has resulted bad experience for the potential customer and it is consider as lost from business aspect.

  Apart from giving a better management system for the admin of the business, it boost the client experience in booking their preferred service. 

  There are two users type in this website, customer and admin. 

  Important things for the customer :

  1. Guide of what needs to do to order the services
  2. Confirmation of order. Keep the customer informed that their order is received and being processed.
  3. Update of the job order status. It is very important to keep customer updated and active communication implies professioanlism of the business.

  Important things for the administrator :

  1. Filter of pending jobs that needs admin to take action so they do not miss out on any job request received 
  2. List out all of the future jobs. It displays all scheduled jobs
  3. Details of each job. Show the customer details, when, and where the jobs take place.
  4. Updating the status of the job order.
  5. Check on the jobs history and client details
---

### Functionality / Features

**Features for Minimum Viable Products**

1. An interactive web application
2. Management system for the administrator. The features include:
   - Admin Accounts. Login ability with the required information
   - Order Submission. Automatically create a new job with all the information provided by the customer
   - Option to create, retrieve, change, and delete job request for the admin user

**Additional Features**

- Integrated payment system to allow user make an online payment

**Extended the system for Customer Side** 

1. Customer User Accounts. Sign Up and Login ability with the required information
2. Customer Dashboard. It includes:
   - Display their job request status
   - Make online payment

### Target Audience : 

The website is best suited for the cleaning and laundry business who wants to grow the number of their customer and improve their quality of services by focusing on delivering their service and lift off the administration work. It is also targeting for any individual who require cleaning and laundry services.



### Tech stack

**Front-End Technologies** : HTML5, CSS, and Jinja

**Back-End Technologies** : Python

**Back-End Frameworks** : Flask

**Database and Database Access Library** : PostgreSQL, Flask SQLAlchemy (Object Relational Mapper), Marshmallow (Serialization)

**Cloud Application Deployment** : AWS (EC2)


### Project Documents
For better understanding about this system, User stories, Data flow and Application architecture diagrams are provided. Please check [HERE](https://github.com/hholly3003/Cleaning-and-Laundry-Management-System/wiki/Documents).