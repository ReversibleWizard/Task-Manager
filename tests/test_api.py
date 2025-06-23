import unittest
from flask_api_server import app
import json

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

    def test_create_task(self):
        payload = {
            "title": "Test Task",
            "description": "Testing task creation",
            "status": "pending",
            "priority": "low"
        }
        response = self.client.post("/api/tasks", data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", response.get_json())

    def test_get_all_tasks(self):
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json())
