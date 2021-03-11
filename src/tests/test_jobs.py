from helpers import Helpers
from models.Job import Job
from models.JobType import JobType
import datetime, random

class TestJobs(Helpers):    
    def test_job_index_admin(self):
        admin_login = {
            "email": "admin@test.com",
            "password": "123456"
        }

        endpoint = "/jobs/"
        
        #get job_index as admin user
        headers_data = self.login(admin_login)
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data)==5)
    
    def test_job_index_user(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }

        endpoint = "/jobs/"

        #get job_index as regular user
        headers_data = self.login(user_login)
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data, list)
        self.assertLess(len(data),5)

    def test_job_create(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }

        endpoint = "/jobs/"
        headers_data = self.login(user_login)
        job_type = JobType.query.get(1)
        data = {
            "cust_name": "John Doe",
            "contact_num": "0412345678",
            "job_created":"2021-03-11T13:28:22.812Z",
            "job_date": "2020-03-30",
            "job_requested" : job_type.name,
            "job_time" : "08:50:01",
            "job_address":"123 Main St Melbourne VIC 3000",
            "job_status":"Pending",
            "job_notes":""
        }

        response, data = self.post_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
        self.assertTrue(bool("id" in data.keys()))
        self.assertEqual(data["job_requested"], "cleaning")

    def test_job_create_invalid_jobtype(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }

        endpoint = "/jobs/"
        headers_data = self.login(user_login)
        data = {
            "cust_name": "John Doe",
            "contact_num": "0412345678",
            "job_created":"2021-03-11T13:28:22.812Z",
            "job_date": "2020-03-30",
            "job_requested" : "testing",
            "job_time" : "08:50:01",
            "job_address":"123 Main St Melbourne VIC 3000",
            "job_status":"Pending",
            "job_notes":""
        }

        response, data = self.post_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertIsNot(data["job_requested"], "cleaning")

    def test_job_id_admin(self):
        admin_login = {
            "email": "admin@test.com",
            "password": "123456"
        }
        job = Job.query.first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(admin_login)
        
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
    
    def test_job_id_user(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }
        job = Job.query.filter_by(profile_id=1).first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(user_login)
        
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
    
    def test_job_id_user_unauthorised(self):
        user_login = {
            "email": "test2@test.com",
            "password": "123456"
        }
        job = Job.query.filter_by(profile_id=1).first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(user_login)
        
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(data)

    def test_job_update(self):
        user_login ={
            "email": "test1@test.com",
            "password": "123456"
        }
        job = Job.query.filter_by(profile_id=1).first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(user_login)
        
        data = {
            "cust_name": "Mark Morgan",
            "contact_num": "0412345678",
            "job_created":"2021-03-11T13:28:22.812Z",
            "job_date": "2020-03-30",
            "job_requested" : "cleaning",
            "job_time" : "08:50:01",
            "job_address":"123 Main St Melbourne VIC 3000",
            "job_status":"Pending",
            "job_notes":""
        }

        response, data = self.patch_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["cust_name"],"Mark Morgan")

    def test_job_update_unauthorised(self):
        user_login ={
            "email": "test2@test.com",
            "password": "123456"
        }
        job = Job.query.filter_by(profile_id=1).first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(user_login)
        
        data = {
            "cust_name": "Mark Morgan",
            "contact_num": "0412345678",
            "job_created":"2021-03-11T13:28:22.812Z",
            "job_date": "2020-03-30",
            "job_requested" : "cleaning",
            "job_time" : "08:50:01",
            "job_address":"123 Main St Melbourne VIC 3000",
            "job_status":"Pending",
            "job_notes":""
        }

        response, data = self.patch_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(data)
    
    # def test_job_delete(self):
    #     admin_login ={
    #         "email": "admin@test.com",
    #         "password": "123456"
    #     }
    #     job = Job.query.first()
    #     endpoint = f"/jobs/{job.id}"
    #     headers_data = self.login(admin_login)

    #     response, data = self.delete_request(endpoint, headers=headers_data)
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertIsNotNone(data)
    #     # self.assertIsInstance(data, dict)
    
    def test_job_delete_invalid(self):
        admin_login ={
            "email": "admin@test.com",
            "password": "123456"
        }
        job = Job.query.first()
        endpoint = f"/jobs/6"
        headers_data = self.login(admin_login)

        response, data = self.delete_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,404)
        self.assertIsNone(data)

    def test_job_delete_unauthorised(self):
        user_login ={
            "email": "test1@test.com",
            "password": "123456"
        }
        job = Job.query.filter_by(profile_id=1).first()
        endpoint = f"/jobs/{job.id}"
        headers_data = self.login(user_login)

        response, data = self.delete_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(data)