import os
from flask import Flask, render_template, request, jsonify
from config import config
from models import db, Task


def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'default'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register all routes with the app."""
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html')

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """Retrieve all tasks."""
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """Create a new task."""
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201

    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """Update a task."""
        task = db.session.get(Task, task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        
        return jsonify(task.to_dict())

    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """Delete a task."""
        task = db.session.get(Task, task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'})


# Create the app instance for running directly
app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Debug mode is controlled by FLASK_DEBUG environment variable
    # Default to False for security; set FLASK_DEBUG=1 for development
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode)
