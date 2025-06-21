from flask import Blueprint, jsonify
from ..utils.db import tasks_collection

stats_bp = Blueprint('stats', __name__, url_prefix='/api')

@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        statuses = ['completed', 'pending', 'in_progress']
        priorities = ['high', 'medium', 'low']
        stats = {
            'total_tasks': tasks_collection.count_documents({}),
            **{f'{s}_tasks': tasks_collection.count_documents({'status': s}) for s in statuses},
            **{f'{p}_priority': tasks_collection.count_documents({'priority': p}) for p in priorities}
        }
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
