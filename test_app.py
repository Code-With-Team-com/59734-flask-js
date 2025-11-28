import pytest
import json
import os
import sys

# Set up the testing environment
os.environ['FLASK_ENV'] = 'testing'

from app import app, db
from models import Task


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def sample_task(client):
    """Create a sample task for testing."""
    response = client.post('/api/tasks',
                          data=json.dumps({'title': 'Test Task', 'description': 'Test Description'}),
                          content_type='application/json')
    return json.loads(response.data)


class TestHomePage:
    """Tests for the home page."""
    
    def test_home_page(self, client):
        """Test that the home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'TechStart Solutions' in response.data


class TestGetTasks:
    """Tests for GET /api/tasks endpoint."""
    
    def test_get_tasks_empty(self, client):
        """Test getting tasks when there are none."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_tasks_with_data(self, client, sample_task):
        """Test getting tasks when there are tasks."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'Test Task'


class TestCreateTask:
    """Tests for POST /api/tasks endpoint."""
    
    def test_create_task_with_title_only(self, client):
        """Test creating a task with only title."""
        response = client.post('/api/tasks',
                              data=json.dumps({'title': 'New Task'}),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'New Task'
        assert data['description'] == ''
        assert data['completed'] == False
        assert 'id' in data
    
    def test_create_task_with_title_and_description(self, client):
        """Test creating a task with title and description."""
        response = client.post('/api/tasks',
                              data=json.dumps({'title': 'New Task', 'description': 'Task description'}),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'New Task'
        assert data['description'] == 'Task description'
    
    def test_create_task_without_title(self, client):
        """Test creating a task without title fails."""
        response = client.post('/api/tasks',
                              data=json.dumps({'description': 'Only description'}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_empty_body(self, client):
        """Test creating a task with empty body fails."""
        response = client.post('/api/tasks',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400


class TestUpdateTask:
    """Tests for PUT /api/tasks/<id> endpoint."""
    
    def test_update_task_title(self, client, sample_task):
        """Test updating a task's title."""
        task_id = sample_task['id']
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'title': 'Updated Title'}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
        assert data['description'] == 'Test Description'  # unchanged
    
    def test_update_task_completed(self, client, sample_task):
        """Test marking a task as completed."""
        task_id = sample_task['id']
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({'completed': True}),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] == True
    
    def test_update_task_not_found(self, client):
        """Test updating a non-existent task fails."""
        response = client.put('/api/tasks/999',
                             data=json.dumps({'title': 'Updated Title'}),
                             content_type='application/json')
        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /api/tasks/<id> endpoint."""
    
    def test_delete_task(self, client, sample_task):
        """Test deleting a task."""
        task_id = sample_task['id']
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # Verify task is deleted
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert len(data) == 0
    
    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task fails."""
        response = client.delete('/api/tasks/999')
        assert response.status_code == 404


class TestTaskModel:
    """Tests for the Task model."""
    
    def test_task_to_dict(self, client):
        """Test that task converts to dictionary correctly."""
        with app.app_context():
            task = Task(title='Test', description='Desc', completed=True)
            db.session.add(task)
            db.session.commit()
            
            task_dict = task.to_dict()
            assert task_dict['title'] == 'Test'
            assert task_dict['description'] == 'Desc'
            assert task_dict['completed'] == True
            assert 'id' in task_dict


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
