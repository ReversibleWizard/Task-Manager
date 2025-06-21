from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
import logging

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['task_manager']
    tasks_collection = db['tasks']
    users_collection = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# Helper functions
def serialize_doc(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
        return doc
    return None

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

# Route: Home (serve frontend)
@app.route('/')
def index():
    return render_template('index.html')

# -------------------- API ROUTES --------------------

# 1. GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        query = {}
        if request.args.get('status'):
            query['status'] = request.args.get('status')
        if request.args.get('priority'):
            query['priority'] = request.args.get('priority')

        tasks = list(tasks_collection.find(query).sort('created_at', -1))
        return jsonify({
            'success': True,
            'data': serialize_docs(tasks),
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 2. POST create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'success': False, 'error': 'Title is required'}), 400

        task = {
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data.get('status', 'pending'),
            'priority': data.get('priority', 'medium'),
            'assigned_to': data.get('assigned_to', ''),
            'due_date': data.get('due_date'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)

        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': serialize_doc(task)
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 3. PUT update a task
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    try:
        data = request.get_json()
        update_fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
        update_data = {f: data[f] for f in update_fields if f in data}
        update_data['updated_at'] = datetime.utcnow()

        result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})
        if result.matched_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404

        updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        return jsonify({'success': True, 'data': serialize_doc(updated_task)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 4. DELETE a task
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    try:
        result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 5. GET a single task
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    return jsonify({'success': True, 'data': serialize_doc(task)}), 200

# 6. GET task stats
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

# -------------------- END --------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)
