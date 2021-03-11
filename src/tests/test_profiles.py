from models.Profile import Profile
from helpers import Helpers

class TestProfiles(Helpers):    
    def test_profile_index(self):
        admin_login = {
            "email": "admin@test.com",
            "password": "123456"
        }
        endpoint = "/profiles/"
        headers_data = self.login(admin_login)
        
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data,list)
        self.assertEqual(len(data),6)
    
    def test_profile_index_unauthorised(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }
        endpoint = "/profiles/"
        headers_data = self.login(user_login)
        
        response, data = self.get_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,403)
        self.assertIsNone(data)
    
    def test_profile_create(self):
        new_user = {
            "email": "test6@test.com",
            "password": "123456"
        }

        user_login = {
            "email": "test6@test.com",
            "password": "123456"
        }
        
        self.register(new_user)
        endpoint = "/profiles/"
        headers_data = self.login(user_login)
        data ={
            "username":user_login["email"],
            "firstname":"Creating",
            "lastname":"Profile"
        }
        
        response, data = self.post_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], 7)
        self.assertEqual(data["firstname"], "Creating")
        self.assertEqual(data["username"],"test6@test.com")
    
    def test_profile_create_exist(self):
        user_login = {
            "email": "test1@test.com",
            "password": "123456"
        }
        endpoint = "/profiles/"
        headers_data = self.login(user_login)
        data ={
            "firstname":"Creating",
            "lastname":"Profile"
        }
        
        response, data = self.post_request(endpoint, headers=headers_data)
        self.assertEqual(response.status_code,400)
        self.assertIsNone(data)

    def test_profile_id_admin(self):
        admin_login = {
            "email": "admin@test.com",
            "password": "123456"
        }
        profile = Profile.query.first()
        endpoint =f"/profiles/{profile.id}"
        headers_data = self.login(admin_login)

        response, data = self.get_request(endpoint,headers=headers_data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data,dict)
    
    def test_profile_id_user(self):
        user_login = {
            "email":"test1@test.com",
            "password":"123456"
        }
        profile = Profile.query.filter_by(id=1).first()
        endpoint =f"/profiles/{profile.id}"
        headers_data = self.login(user_login)

        response, data = self.get_request(endpoint,headers=headers_data)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(data,dict)
    
    def test_profile_id_user_unauthorised(self):
        user_login = {
            "email":"test1@test.com",
            "password":"123456"
        }
        profile = Profile.query.filter_by(id=2).first()
        endpoint =f"/profiles/{profile.id}"
        headers_data = self.login(user_login)

        response, data = self.get_request(endpoint,headers=headers_data)
        self.assertEqual(response.status_code,401)
        self.assertIsNone(data)
    
    def test_profile_id_not_exist(self):
        new_user = {
            "email": "test7@test.com",
            "password": "123456"
        }
        user_login = {
            "email":"test7@test.com",
            "password":"123456"
        }
        self.register(new_user)
        endpoint =f"/profiles/7"
        headers_data = self.login(user_login)

        response, data = self.get_request(endpoint,headers=headers_data)
        self.assertEqual(response.status_code,400)
        self.assertIsNone(data)

    def test_profile_update(self):
        user_login ={
            "email": "test1@test.com",
            "password": "123456"
        }

        profile = Profile.query.get(1)
        endpoint = f"/profiles/{profile.id}"
        headers_data = self.login(user_login)
        data = {
            "username" : "test1@test.com",
            "firstname" : "Mark",
            "lastname" : "Morgan"
        }
        
        response, data = self.patch_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["firstname"],"Mark")
        self.assertEqual(data["lastname"],"Morgan")
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["username"],"test1@test.com")

    def test_profile_update_unauthorised(self):
        user_login ={
            "email": "test2@test.com",
            "password": "123456"
        }
        profile = Profile.query.get(1)
        endpoint = f"/profiles/{profile.id}"
        headers_data = self.login(user_login)
        
        data = {
            "username" : "test1@test.com",
            "firstname" : "Mark",
            "lastname" : "Morgan"
        }

        response, data = self.patch_request(endpoint, headers=headers_data, body=data)
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(data)
    
    # def test_profile_delete_admin(self):
    #     admin_login = {
    #         "email": "admin@test.com",
    #         "password": "123456"
    #     }
    #     profile = Profile.query.get(1)
    #     endpoint =f"/profiles/{profile.id}"
    #     headers_data = self.login(admin_login)

    #     response, data = self.delete_request(endpoint, headers=headers_data)
    #     self.assertEqual(response.status_code, 200)
        # self.assertIsNotNone(data)
        # self.assertIsInstance(data, dict)