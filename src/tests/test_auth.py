from models.User import User
from helpers import Helpers

class TestAuth(Helpers):
    def test_register(self):
        endpoint ="/auth/register"
        data = {
            "email" : "example@test.com",
            "password" : "112233"
        }
        
        response, data = self.post_request(endpoint, body=data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(data["id"], 7)
        self.assertEqual(data["is_admin"], False)
        self.assertEqual(data["email"], "example@test.com")
    
    def test_register_existing_user(self):
        endpoint ="/auth/register"
        data = {
            "email" : "test1@test.com",
            "password" : "112233"
        }

        response, data = self.post_request(endpoint, body=data)
        self.assertEqual(response.status_code,400)
        self.assertIsNone(data)
    
    def test_login(self):
        endpoint = "/auth/login"
        data = {
            "email" : "test1@test.com",
            "password" : "123456"
        }

        response, data = self.post_request(endpoint, body=data)
        self.assertEqual(response.status_code,200)
        self.assertIn("token", data)
    
    def test_login_unauthorised(self):
        endpoint = "/auth/login"
        data = {
            "email" : "test1@test.com",
            "password" : "12345678"
        }

        response, data = self.post_request(endpoint, body=data)
        self.assertEqual(response.status_code,401)
        self.assertIsNone(data)