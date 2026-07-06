from flask import Flask, redirect, url_for
from flask_cors import CORS
from routes import student_routes
from database import get_db_connection
from analytics import generate_analytics_report
import os

# Serve the frontend from the 'frontend' directory
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend'), static_url_path='/')
CORS(app)

# Register the blueprint for API routes
app.register_blueprint(student_routes, url_prefix='/api')

@app.route('/')
def index():
    """Redirects the root URL to the dashboard."""
    return redirect(url_for('static', filename='dashboard.html'))

def initialize_app():
    """Checks for database connection and generates initial analytics report if needed."""
    # 1. Test database connection
    db_conn = get_db_connection()
    if db_conn:
        print("Database connection successful.")
        db_conn.close()
    else:
        print("Database connection failed. Please check your MySQL server and credentials.")
        # Exit if DB connection fails, as the app is unusable.
        return False

    # 2. Ensure reports directory exists
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(report_dir, exist_ok=True)
    
    # 3. Generate a fresh analytics report on every startup
    # This ensures the dashboard always has data to load.
    print("Generating analytics report on startup...")
    try:
        generate_analytics_report()
    except Exception as e:
        print(f"Error generating analytics report on startup: {e}")
    
    return True

if __name__ == '__main__':
    if initialize_app():
        app.run(debug=True, host='0.0.0.0')
    else:
        print("Application initialization failed. Exiting.")
