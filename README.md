# TechStart Solutions - Task Management System

## Company Story

**TechStart Solutions** is a rapidly growing software development company that has recently secured a major contract with a Fortune 500 client. The management team has assembled a talented group of developers (you and your team!) to build a critical internal tool that will revolutionize how they manage their projects.

## The Challenge

During the kickoff meeting, the CEO shared their vision: *"We need a modern, efficient task management system that our teams can use to track project deliverables. Our current solution is outdated and doesn't meet our needs anymore."*

The Product Owner provided detailed requirements for the MVP (Minimum Viable Product):

### Required Functionality

Your team needs to build a **Task Management System** with the following features:

1. **Task Creation**
   - Users must be able to create new tasks with a title (required) and description (optional)
   - Tasks should be stored persistently in a database

2. **Task Display**
   - All tasks should be displayed in an organized, easy-to-read format
   - The interface should be clean and modern
   - Tasks should show their title, description, and completion status

3. **Task Management**
   - Users must be able to mark tasks as complete/incomplete
   - Users must be able to delete tasks they no longer need
   - The interface should update dynamically without page refreshes

4. **Technical Requirements**
   - Backend: Python with Flask framework
   - Frontend: Vanilla JavaScript (no heavy frameworks initially)
   - Database: SQLite for simplicity and portability
   - RESTful API architecture for frontend-backend communication

5. **User Experience**
   - Responsive design that works on desktop and mobile devices
   - Intuitive interface requiring minimal training
   - Visual feedback for user actions
   - Professional appearance matching our company brand

## Project Setup

This boilerplate provides the folder structure and file templates for you to implement the features.

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd boilerplate-python-js
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start implementing:
   - Set up your Flask app in `app.py`
   - Define your database models in `models.py`
   - Create your frontend in `templates/index.html`
   - Add styles in `static/css/style.css`
   - Add JavaScript functionality in `static/js/main.js`

## Project Structure

```
boilerplate-python-js/
├── app.py                 # Flask application (TODO: implement)
├── models.py              # Database models (TODO: implement)
├── config.py              # Configuration settings (TODO: implement)
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template (TODO: implement)
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet (TODO: implement)
│   └── js/
│       └── main.js       # JavaScript (TODO: implement)
├── README.md             # Project documentation
└── WHATTODO.md           # Action items and tasks
```

## API Endpoints to Implement

You should create the following RESTful API endpoints:

- `GET /api/tasks` - Retrieve all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

## Next Steps

For detailed information about your immediate tasks and action items, please refer to the [WHATTODO.md](WHATTODO.md) file.