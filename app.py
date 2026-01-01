import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- App Setup ---
app = Flask(__name__)

# Configure the database
# Gets the absolute path of the current file's directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Creates the 'instance' directory if it doesn't exist
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
class Task(db.Model):
    """
    Task Model
    - id: Primary Key
    - title: Task title (required)
    - description: Task details (optional)
    - completed: Boolean status
    - priority: String (Low, Medium, High)
    - created_at: Timestamp of creation
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(50), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

    def to_dict(self):
        """Serializes the Task object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            # Format datetime to ISO 8601 string for JSON compatibility
            'created_at': self.created_at.isoformat()
        }

# --- Main Route ---
@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/api/tasks/breakdown', methods=['POST'])
def breakdown_task():
    """Generate subtasks for a given task using simple rules."""
    data = request.json
    task_title = data.get('title', '')
    
    # Simple rule-based subtask generation
    subtasks = []
    
    # Research phase
    subtasks.append(f"Research requirements for: {task_title}")
    subtasks.append(f"Gather necessary resources for: {task_title}")
    
    # Planning phase
    subtasks.append(f"Create detailed plan for: {task_title}")
    subtasks.append(f"Define milestones for: {task_title}")
    
    # Execution phase
    subtasks.append(f"Implement core features of: {task_title}")
    subtasks.append(f"Test and validate: {task_title}")
    
    # Review phase
    subtasks.append(f"Review and refine: {task_title}")
    subtasks.append(f"Document progress on: {task_title}")
    
    return jsonify({"subtasks": subtasks})

# --- API Routes ---

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    API endpoint to get tasks.
    Supports filtering, searching, and sorting via query parameters.
    """
    try:
        # Start with all tasks
        query = Task.query

        # Filtering
        filter_by = request.args.get('filter', 'all').lower()
        if filter_by == 'active':
            query = query.filter_by(completed=False)
        elif filter_by == 'completed':
            query = query.filter_by(completed=True)

        # Searching
        search_term = request.args.get('search', '').strip()
        if search_term:
            # Case-insensitive search on title and description
            query = query.filter(
                db.or_(
                    Task.title.ilike(f'%{search_term}%'),
                    Task.description.ilike(f'%{search_term}%')
                )
            )

        # Sorting
        sort_by = request.args.get('sort', 'date_desc').lower()
        if sort_by == 'date_asc':
            query = query.order_by(Task.created_at.asc())
        elif sort_by == 'date_desc':
            query = query.order_by(Task.created_at.desc())
        elif sort_by == 'priority':
            # Order by priority: High, Medium, Low
            priority_order = db.case(
                (Task.priority == 'High', 1),
                (Task.priority == 'Medium', 2),
                (Task.priority == 'Low', 3),
                else_=4
            )
            query = query.order_by(priority_order.asc(), Task.created_at.desc())
        elif sort_by == 'status':
            query = query.order_by(Task.completed.asc(), Task.created_at.desc())
        else:
            # Default sort
            query = query.order_by(Task.created_at.desc())

        tasks = query.all()

        # Get counts *before* serialization
        total_tasks = Task.query.count()
        pending_tasks = Task.query.filter_by(completed=False).count()
        completed_tasks = Task.query.filter_by(completed=True).count()

        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'counts': {
                'total': total_tasks,
                'pending': pending_tasks,
                'completed': completed_tasks
            }
        }), 200

    except Exception as e:
        print(f"Error in get_tasks: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """API endpoint to add a new task."""
    try:
        data = request.get_json()

        # Validation
        if not data or 'title' not in data or not data['title'].strip():
            return jsonify({'error': 'Title is required.'}), 400

        title = data['title'].strip()
        description = data.get('description', '').strip()
        priority = data.get('priority', 'Medium')

        if priority not in ['Low', 'Medium', 'High']:
            priority = 'Medium'

        new_task = Task(
            title=title,
            description=description,
            priority=priority
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify(new_task.to_dict()), 201 # 201 Created

    except Exception as e:
        db.session.rollback()
        print(f"Error in add_task: {e}")
        return jsonify({'error': 'Failed to add task.'}), 500

@app.route('/api/task/<int:id>', methods=['PUT'])
def update_task(id):
    """
    API endpoint to update an existing task.
    Used for editing title, description, priority, or toggling completion.
    """
    try:
        task = db.session.get(Task, id)
        if not task:
            return jsonify({'error': 'Task not found.'}), 404

        data = request.get_json()

        # Update fields if they exist in the request data
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': 'Title cannot be empty.'}), 400
            task.title = title

        if 'description' in data:
            task.description = data['description'].strip()

        if 'priority' in data:
            priority = data['priority']
            if priority not in ['Low', 'Medium', 'High']:
                return jsonify({'error': 'Invalid priority.'}), 400
            task.priority = priority

        if 'completed' in data:
            if not isinstance(data['completed'], bool):
                 return jsonify({'error': 'Invalid completed status.'}), 400
            task.completed = data['completed']

        db.session.commit()
        return jsonify(task.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in update_task: {e}")
        return jsonify({'error': 'Failed to update task.'}), 500

@app.route('/api/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    """API endpoint to delete a single task."""
    try:
        task = db.session.get(Task, id)
        if not task:
            return jsonify({'error': 'Task not found.'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully.'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_task: {e}")
        return jsonify({'error': 'Failed to delete task.'}), 500

@app.route('/api/tasks/clear-completed', methods=['DELETE'])
def clear_completed_tasks():
    """API endpoint to delete all completed tasks."""
    try:
        num_deleted = db.session.query(Task).filter_by(completed=True).delete()
        db.session.commit()

        return jsonify({
            'message': f'Successfully cleared {num_deleted} completed tasks.'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in clear_completed_tasks: {e}")
        return jsonify({'error': 'Failed to clear completed tasks.'}), 500

# --- Utility ---
def create_database(app_context):
    """Creates database tables if they don't exist."""
    with app_context:
        db.create_all()
    print("Database tables created.")

# --- Run Application ---
if __name__ == '__main__':
    # Create the database tables on first run
    create_database(app.app_context())
    # Run the app in debug mode
    app.run(debug=True)