from flask import Blueprint, request, jsonify
from bson import ObjectId
from ..utils.db import tasks_collection
from ..utils.helpers import serialize_doc, serialize_docs, is_valid_object_id
from datetime import datetime

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@task_bp.route('', methods=['GET'])
def get_tasks():
    try:
        query = {k: v for k, v in request.args.items() if k in ['status', 'priority']}
        tasks = list(tasks_collection.find(query).sort('created_at', -1))
        return jsonify({'success': True, 'data': serialize_docs(tasks), 'count': len(tasks)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('', methods=['POST'])
def create_task():
    try:
        data = request.get_json(force=True)
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
        return jsonify({'success': True, 'message': 'Task created successfully', 'data': task}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    if not is_valid_object_id(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    try:
        data = request.get_json(force=True)
        update_fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
        update_data = {f: data[f] for f in update_fields if f in data}
        update_data['updated_at'] = datetime.utcnow()
        result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})
        if result.matched_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        return jsonify({'success': True, 'message': 'Task updated successfully', 'data': serialize_doc(updated_task)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not is_valid_object_id(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    try:
        result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        return jsonify({'success': True, 'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    if not is_valid_object_id(task_id):
        return jsonify({'success': False, 'error': 'Invalid task ID'}), 400
    try:
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        return jsonify({'success': True, 'data': serialize_doc(task)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
