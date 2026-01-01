from app import app, db

# Create all database tables
with app.app_context():
    db.create_all()
    print("Database initialized successfully!")