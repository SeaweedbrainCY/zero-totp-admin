import unittest
from main import app,db
from unittest.mock import patch
from environment.configuration import conf
from uuid import uuid4
import os



class TestLogin(unittest.TestCase):
    def setUp(self):
        self.application = app.app
        self.client = app.test_client()
    
    
    def test_GET_endpoint_requiring_session(self):
        get_endpoints = ["/api/v1/whoami", "/api/v1/stats/users/category", "/api/v1/stats/users/timechart", "/api/v1/stats/server/rate-limiting", "/api/v1/users/all", "/api/v1/users/1", "/api/v1/notifications/all", "/api/v1/notification/07b294ac-88d6-4c36-8e26-7d06c28f8228"]
        for get_endpoint in get_endpoints:
            with self.application.app_context():
                response = self.client.get(get_endpoint)
                self.assertEqual(response.status_code, 401, f"GET {get_endpoint} should return 401. Got {response.status_code}")
    
    def test_PUT_endpoint_requiring_session(self):
        put_endpoints = ["/api/v1/users/block/1", "/api/v1/users/unblock/1", "/api/v1/notification/07b294ac-88d6-4c36-8e26-7d06c28f8228"]
        for put_endpoint in put_endpoints:
            with self.application.app_context():
                response = self.client.put(put_endpoint)
                self.assertEqual(response.status_code, 401, f"PUT {put_endpoint} should return 401. Got {response.status_code}")

    def test_DELETE_endpoint_requiring_session(self):
        put_endpoints = ["/api/v1/users/1", "/api/v1/notification/07b294ac-88d6-4c36-8e26-7d06c28f8228"]
        for put_endpoint in put_endpoints:
            with self.application.app_context():
                response = self.client.delete(put_endpoint)
                self.assertEqual(response.status_code, 401, f"DELETE {put_endpoint} should return 401. Got {response.status_code}")
    
    def test_POST_endpoint_requiring_session(self):
        put_endpoints = ["/api/v1/notification"]
        for put_endpoint in put_endpoints:
            with self.application.app_context():
                response = self.client.post(put_endpoint)
                self.assertEqual(response.status_code, 401, f"POST {put_endpoint} should return 401. Got {response.status_code}")

        