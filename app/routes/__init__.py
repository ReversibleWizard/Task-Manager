from .task_routes import task_bp
from .stats_routes import stats_bp

def register_routes(app):
    app.register_blueprint(task_bp)
    app.register_blueprint(stats_bp)
