import unittest
from flask_api_server import validate_task_data

class LogicUnitTestCase(unittest.TestCase):
    def test_valid_task_input(self):
        data = {"title": "Read Book"}
        valid, message = validate_task_data(data)
        self.assertTrue(valid)

    def test_missing_title(self):
        data = {}
        valid, message = validate_task_data(data)
        self.assertFalse(valid)
        self.assertEqual(message, "Title is required")