# Student Analytics Project

This project is a simple Student Analytics application built with Flask for the backend, HTML/CSS/JavaScript for the frontend, and MySQL for the database. It allows for basic CRUD (Create, Read, Update, Delete) operations on student records and generates analytical reports with AI-powered insights.

## Technologies Used

*   **Frontend**: HTML, CSS, JavaScript, Bootstrap, Chart.js
*   **Backend**: Python (Flask)
*   **Database**: MySQL
*   **Analytics**: Pandas, NumPy
*   **AI Insights**: Google Gemini API
*   **Environment Management**: python-dotenv

## Development Roadmap

The following steps from the original roadmap have been completed:

*   **Step 1: Create the basic website**: Dashboard, Add Student form, Student List, and Analytics page.
*   **Step 2: Connect the website to the MySQL database**: Integrated `mysql-connector-python` and ensured automatic database/table creation.
*   **Step 3: Implement CRUD operations**:
    *   Add student (`POST /api/students/add`)
    *   View students (`GET /api/students`, `GET /api/students/<id>`)
    *   Edit student (`PUT /api/students/<id>`)
    *   Delete student (`DELETE /api/students/<id>`)
*   **Step 4: Create the analytics engine**: Reads student data, cleans it, calculates KPIs (total students, average age, students per grade), and generates a JSON report (`reports/latest_report.json`).
*   **Step 5: Build APIs to serve the analytics JSON**: `GET /api/analytics` endpoint serves the generated report.
*   **Step 6: Display KPIs and charts on the dashboard**: The `dashboard.html` dynamically fetches and displays analytics data, including a bar chart for student grades.
*   **Step 7: Add AI-generated insights and recommendations**: Integrated Google Gemini API to generate insights based on the analytics report.

## Key Changes Implemented

During the development, several key files were modified or created:

*   `backend/database.py`: Enhanced `get_db_connection` to automatically create the `student_analytics` database and the `students` table if they don't exist.
*   `backend/app.py`: Modified to test the database connection upon application startup, ensuring database availability.
*   `backend/analytics.py`:
    *   Implemented the analytics engine using Pandas and NumPy to calculate KPIs.
    *   Integrated the Google Gemini API for generating AI-powered insights, loading the API key from a `.env` file.
    *   Added logic to handle cases where no student data is available.
*   `backend/.env`: Created to securely store the Google Gemini API key.
*   `requirements.txt`: Updated to include `google-generativeai` and `python-dotenv` for AI insights and environment variable management.
*   `frontend/dashboard.html`: Updated to fetch and display dynamic analytics data, including Chart.js integration for visualizations and AI insights.
*   `frontend/students.html`, `frontend/add_student.html`, `frontend/edit_student.html`: Implemented JavaScript to interact with the backend CRUD APIs.

## Setup Instructions

1.  **MySQL Server**: Ensure you have a MySQL server running. The application uses `localhost`, `user='root'`, and an empty password by default. If your MySQL configuration is different, you will need to modify `backend/database.py` accordingly.
2.  **Install Dependencies**: Navigate to the project's root directory in your terminal and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Google Gemini API Key (Optional)**: To enable AI-generated insights, obtain an API key from Google AI Studio. Then, create or open the `backend/.env` file and add your key:
    ```
    # backend/.env
    GEMINI_API_KEY="your_actual_gemini_api_key"
    ```

## How to Run the Application

1.  **Start your MySQL Server**: Ensure your MySQL server is running.
2.  **Run the Backend**: Open a terminal in the project's root directory and run the Flask application:
    ```bash
    python backend/app.py
    ```
    This will start the Flask server, typically on `http://127.0.0.1:5000`.
3.  **Open the Frontend**: Open the `frontend/dashboard.html` file in your web browser. You can also navigate to other pages using the navbar.

## How to Use the Application

*   **View Students**: Navigate to the "Students" page (accessible via `frontend/students.html` or the navbar) to see a list of all enrolled students.
*   **Add a Student**: Go to the "Add Student" page (`frontend/add_student.html`) and fill out the form to add new student records.
*   **Edit/Delete a Student**: On the "Students" page, each student entry has "Edit" and "Delete" buttons.
    *   Click "Edit" to modify a student's details.
    *   Click "Delete" to remove a student record (confirmation will be requested).
*   **View Analytics**: The "Dashboard" page (`frontend/dashboard.html`) displays key performance indicators (KPIs) such as total students and average age, along with a bar chart showing student distribution per grade.
*   **Generate Analytics Report**: The analytics report is generated by `backend/analytics.py`. To ensure the dashboard shows the latest data (especially after adding/editing/deleting students), you should manually run this script:
    ```bash
    python backend/analytics.py
    ```
    After running this, refresh your browser on the Dashboard page to see updated analytics.
*   **AI Insights**: On the Dashboard, AI-generated insights will appear if you have configured your OpenAI API key in `backend/.env` and regenerated the analytics report.
*   **AI Insights**: On the Dashboard, AI-generated insights will appear if you have configured your **Google Gemini API key** in `backend/.env` and regenerated the analytics report.
