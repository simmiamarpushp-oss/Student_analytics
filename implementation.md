# Student Analytics Project Implementation Guide

This document provides a step-by-step guide to set up, run, and understand the Student Analytics project.

## 1. Project Overview

The project is a web application for managing and analyzing student data.

-   **Frontend**: The user interface for viewing, adding, and editing student data and analytics.
-   **Backend**: A Python Flask server that handles business logic, data processing, and serves the frontend.
-   **Database**: A MySQL database to store student records.

## 2. Technologies Used

-   **Frontend**: HTML, CSS, JavaScript, Bootstrap, Chart.js
-   **Backend**: Python, Flask
-   **Database**: MySQL
-   **Analytics**: Pandas, NumPy

## 3. Setup and Installation

Follow these steps to get the project running on your local machine.

### Step 3.1: Set up the Database (XAMPP & MySQL)

1.  **Start XAMPP**: Open the XAMPP Control Panel and start the **Apache** and **MySQL** modules.
2.  **Open phpMyAdmin**: Click the "Admin" button for the MySQL module. This will open phpMyAdmin in your browser (`http://localhost/phpmyadmin`).
3.  **Create Database**:
    -   Click on the **Databases** tab.
    -   Under "Create database", enter `student_analytics` and click **Create**.
4.  **Import SQL Table**:
    -   Select the `student_analytics` database from the left-hand menu.
    -   Click on the **Import** tab.
    -   Click "Choose File" and select the `database/students.sql` file from this project.
    -   Click **Go** at the bottom of the page to import the table structure.

### Step 3.2: Set up the Backend (Python)

1.  **Install Python**: If you don't have Python, download and install it from [python.org](https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during installation.

2.  **Open a Terminal**: Navigate to the project's root directory (`c:/xampp/htdocs/student-analytics`) in your terminal or command prompt.

3.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    ```
    And activate it:
    -   **Windows**: `venv\Scripts\activate`
    -   **macOS/Linux**: `source venv/bin/activate`

4.  **Install Dependencies**: Install all the required Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment**:
    -   In the `backend/` folder, there is a file named `.env`. This file holds the database connection details.
    -   Open `backend/.env` and make sure it looks like this. The default XAMPP MySQL setup has no password for the root user.
    ```
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=student_analytics
    ```

### Step 3.3: Run the Application

1.  **Start the Backend Server**:
    -   Make sure your terminal is still in the project's root directory and the virtual environment is active.
    -   Run the main application file:
    ```bash
    python backend/app.py
    ```
2.  **View the Frontend**:
    -   Once the server is running, you will see output in the terminal, including a URL like `http://127.0.0.1:5000` or `http://localhost:5000`.
    -   Open your web browser and go to **`http://localhost:5000/dashboard.html`**.

    > **Note**: The "Not Found" error you saw before was because the Python server didn't know how to serve the HTML files. The next step will be to modify the `app.py` file to fix this.

## 4. How It Works: The Flow

1.  When you run `python backend/app.py`, the Flask web server starts.
2.  The server is configured to treat the `frontend` folder as the source for all web pages.
3.  When you open `http://localhost:5000/dashboard.html` in your browser, the Flask server finds `dashboard.html` in the `frontend` folder and sends it to your browser.
4.  The HTML, CSS, and JavaScript files work together in your browser to create the user interface.
5.  When you perform actions (like adding a student), the JavaScript code sends requests to API endpoints defined in `backend/routes.py`.
6.  The backend code processes these requests, interacts with the MySQL database, and sends back a response.
7.  The analytics engine (`analytics.py`) is triggered by a specific API call to process all student data and save the results in `reports/latest_report.json`.
8.  The dashboard page periodically fetches this JSON report to update the charts and KPIs automatically.
