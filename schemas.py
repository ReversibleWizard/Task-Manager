from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_api_server import app

ma = Marshmallow(app)

class TaskSchema(ma.Schema):
    class Meta:
        fields = ("_id", "title", "description", "status", "priority", "assigned_to", "due_date")

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
