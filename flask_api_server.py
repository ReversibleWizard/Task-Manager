from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from marshmallow import fields
import os
import logging

# Load environment variables
load_dotenv()

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='docs')
CORS(app)

# Swagger/OpenAPI config
app.config["API_TITLE"] = "Task Manager API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
ma = Marshmallow(app)

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
    db = client['task_manager']
    tasks_collection = db['tasks']
    users_collection = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# ---------- Utility Logic ----------
def validate_task_data(data):
    if "title" not in data or not data["title"].strip():
        return False, "Title is required"
    return True, None

def serialize_doc(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
        return doc
    return None

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

@app.route('/')
def index():
    return render_template('index.html')

# Marshmallow schema
class TaskSchema(ma.Schema):
    _id = fields.String(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    status = fields.String()
    priority = fields.String()
    assigned_to = fields.String()
    due_date = fields.String()

    class Meta:
        ordered = True
        fields = ("_id", "title", "description", "status", "priority", "assigned_to", "due_date")
        required = ("title",)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# API Blueprint using Flask-Smorest
blp = Blueprint("tasks", "tasks", url_prefix="/api/tasks", description="Operations on tasks")

@blp.route("/")
class TaskListResource(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        query = {}
        if request.args.get('status'):
            query['status'] = request.args.get('status')
        if request.args.get('priority'):
            query['priority'] = request.args.get('priority')
        tasks = list(tasks_collection.find(query).sort('created_at', -1))
        for task in tasks:
            task['_id'] = str(task['_id'])
        return tasks

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, new_data):
        result = tasks_collection.insert_one(new_data)
        new_data['_id'] = str(result.inserted_id)
        return new_data

@blp.route("/<string:task_id>")
class TaskResource(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        if not ObjectId.is_valid(task_id):
            return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        task['_id'] = str(task['_id'])
        return task

    @blp.arguments(TaskSchema)
    @blp.response(200, TaskSchema)
    def put(self, update_data, task_id):
        if not ObjectId.is_valid(task_id):
            return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
        update_data['updated_at'] = datetime.utcnow()
        result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})
        if result.matched_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        update_data['_id'] = task_id
        return update_data

    def delete(self, task_id):
        if not ObjectId.is_valid(task_id):
            return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
        result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        return jsonify({'success': True, 'message': 'Task deleted successfully'})

api.register_blueprint(blp)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            'success': True,
            'data': {
                'total_tasks': tasks_collection.count_documents({}),
                'completed_tasks': tasks_collection.count_documents({'status': 'completed'}),
                'pending_tasks': tasks_collection.count_documents({'status': 'pending'}),
                'in_progress_tasks': tasks_collection.count_documents({'status': 'in_progress'}),
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
