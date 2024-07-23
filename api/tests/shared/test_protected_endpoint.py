import unittest
from main import app,db
from unittest.mock import patch
from environment.configuration import conf
from uuid import uuid4
import os
from hashlib import scrypt
from base64 import b64encode
import pytest


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.application = app.app
        self.client = app.test_client()
    
    
    def test_GET_endpoint_requiring_session(self):
        get_endpoints = ["/api/v1/whoami", "/api/v1/stats/users/category", "/api/v1/stats/users/timechart", "/api/v1/stats/server/rate-limiting"]
        for get_endpoint in get_endpoints:
            with self.application.app_context():
                response = self.client.get(get_endpoint)
                self.assertEqual(response.status_code, 401, f"GET {get_endpoint} should return 401. Got {response.status_code}")

        