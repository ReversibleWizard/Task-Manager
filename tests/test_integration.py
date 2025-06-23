import unittest
from pymongo import MongoClient
from flask_api_server import app

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["taskmanager"]
        self.tasks = self.db["tasks"]
        self.api_client = app.test_client()

    def tearDown(self):
        self.tasks.delete_many({})

    def test_create_and_fetch_task(self):
        self.api_client.post("/api/tasks", json={
            "title": "Integration Task",
            "status": "pending",
            "priority": "medium"
        })
        response = self.api_client.get("/api/tasks")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['data']) > 0)
