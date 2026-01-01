ZenTask - A Modern Flask To-Do Web Application
ZenTask is a production-ready, feature-rich To-Do web application built with Flask and SQLAlchemy on the backend, and a
stunning, responsive frontend powered by Tailwind CSS and vanilla JavaScript.
It's designed to be a portfolio-worthy project that showcases modern web development practices, including a RESTful API,
AJAX-driven UI updates, and a premium, SaaS-like design with glassmorphism, dark/light modes, and smooth animations.

✨ Features
Full CRUD Operations: Add, Edit, and Delete tasks effortlessly.
Modern GUI: Stunning, responsive interface with glassmorphism effects, gradients, and dark/light modes.
AJAX-Powered: No page reloads! The UI is updated dynamically via asynchronous API calls.
Task Priorities: Assign Low, Medium, or High priority to tasks, visualized with color codes.
Complete/Incomplete: Toggle task status with a custom-styled checkbox and smooth animations.
Real-time Dashboard: Stats cards show Total, Pending, and Completed tasks, plus a live progress bar.
Powerful Filtering: Filter tasks by All, Active, or Completed status.
Dynamic Search: Instantly search tasks by title or description.
Robust Sorting: Sort tasks by Date (Newest/Oldest), Priority, or Status.
Toast Notifications: Get instant, non-intrusive feedback for all actions.
Confirmation Modals: Custom confirmation dialog prevents accidental deletions.
Persistent Storage: All tasks are saved in a robust SQLite database using the SQLAlchemy ORM.
Responsive Design: Looks and works great on mobile, tablet, and desktop.
Theme Persistence: Your dark/light mode preference is saved in localStorage.
🛠️ Technology Stack
Backend:
Flask: A lightweight Python web framework.
Flask-SQLAlchemy: A Flask extension for easy database management with SQLAlchemy ORM.
SQLite: A serverless, self-contained SQL database engine.
Frontend:
HTML5: Semantic markup for structure.
Tailwind CSS: A utility-first CSS framework for rapid, custom UI design (loaded via CDN).
Vanilla JavaScript (ES6+): For all interactivity, DOM manipulation, and API calls (AJAX/Fetch).
Font Awesome 6: For clean, modern icons (loaded via CDN).
Google Fonts (Poppins): For beautiful typography.
🚀 Getting Started
Follow these instructions to get the project up and running on your local machine.

1. Prerequisites
Python 3.8 or newer
pip (Python package installer)
virtualenv (recommended)
2. Installation & Setup
Clone the repository:
git clone https://github.com/AryanPatel03/To-Do-App.git
cd flask-todo-app

Create and activate a virtual environment:

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
.\venv\Scripts\activate

Install the dependencies:
pip install -r requirements.txt

Run the application:
python app.py

The application will automatically create the instance/tasks.db file and its tables on the first run.

Open the app in your browser: Navigate to http://127.0.0.1:5000

📁 Project Structure
flask-todo-app/
├── app.py # Main Flask application (backend logic, API)
├── requirements.txt # Python dependencies
├── README.md # This file
├── .gitignore # Files to ignore in Git
├── templates/
│ └── index.html # The single-page HTML file (contains all HTML, CSS, JS)
└── instance/
└── tasks.db # SQLite database file (auto-generated)

Note: For this self-contained example, all frontend code (HTML, CSS via Tailwind, and JS) is located in templates/index.html.

🔌 API Endpoints
The frontend communicates with the Flask backend via a RESTful API.

Method	Endpoint	Description
GET	/	Renders the main index.html page.
GET	/api/tasks	Fetches all tasks. Supports query params: filter, sort, search.
POST	/api/tasks	Adds a new task. Expects JSON payload.
PUT	/api/task/<id>	Updates a task (for editing or toggling complete). Expects JSON payload.
DELETE	/api/task/<id>	Deletes a single task.
DELETE	/api/tasks/clear-completed	Deletes all tasks marked as completed.
🌐 Deployment
Deploying to Render (Recommended)
Sign up for a free account at Render.com.
Create a new "Web Service" and connect your GitHub repository.
Settings:
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn "app:app" (You'll need to add gunicorn to your requirements.txt file first: pip freeze > requirements.txt)
Click "Create Web Service". Render will automatically deploy your app.
📈 Future Enhancements
User Authentication: Add user accounts (login/register) so tasks are private.
Due Dates: Add a calendar picker for setting task due dates.
Drag-and-Drop: Allow users to reorder tasks by dragging them.
Categories/Tags: Add tags or project categories to tasks.
Subtasks: Implement a nested subtask system.
Export: Allow users to export their tasks to CSV or JSON.
🤝 Contributing
Contributions are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
