import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv
from database import get_db_connection

try:
    import google.generativeai as genai
except ModuleNotFoundError:
    genai = None

def generate_ai_insights(report):
    """
    Generates AI-powered insights based on the analytics report using the Google Gemini API.
    """
    # Explicitly load the .env file from the backend directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "AI insights could not be generated. Please configure your GEMINI_API_KEY in the backend/.env file."

    if genai is None:
        return "AI insights could not be generated because the optional google-generativeai package is not installed."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Given the following student analytics report, provide some brief, actionable insights for an educational institution.
        The tone should be professional and encouraging.

        Report:
        - Total Students: {report.get('total_students', 'N/A')}
        - Average Age: {report.get('average_age', 'N/A')}
        - Student Distribution by Grade: {json.dumps(report['students_per_grade'])}

        Insights:
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Error generating AI insights: {e}")
        return "An error occurred while generating AI insights. Please check the backend console for details."


def generate_analytics_report():
    """
    Reads student data from the database, calculates analytics,
    and saves a JSON report.
    """
    conn = get_db_connection()
    if not conn:
        print("Failed to get database connection.")
        return

    try:
        # Read data from database into a pandas DataFrame
        df = pd.read_sql("SELECT * FROM students", conn)
        conn.close()

        # Data Cleaning (if necessary)
        df.dropna(inplace=True)

        if df.empty:
            print("No student data found to generate analytics.")
            # create an empty report
            report = {
                'total_students': 0,
                'average_age': 0,
                'students_per_grade': {},
                'ai_insights': 'No student data to generate insights from.'
            }
        else:
            # Calculate KPIs
            total_students = int(df.shape[0])
            average_age = float(df['age'].mean())
            
            students_per_grade = df['grade'].value_counts().to_dict()
            for key, value in students_per_grade.items():
                students_per_grade[key] = int(value)


            # Prepare the report
            report = {
                'total_students': total_students,
                'average_age': round(average_age, 2),
                'students_per_grade': students_per_grade,
            }

            # Generate AI insights, with fallback for errors
            try:
                report['ai_insights'] = generate_ai_insights(report)
            except Exception as ai_error:
                print(f"Could not generate AI insights due to an error: {ai_error}")
                report['ai_insights'] = f"AI insights could not be generated. Error: {ai_error}"

        # Define the absolute path for the report file
        # This ensures it's always created in the project's root `reports` directory
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, 'latest_report.json')

        # Save the report as a JSON file
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        
        print("Analytics report generated successfully.")

    except Exception as e:
        print(f"An error occurred during analytics generation: {e}")
        # Do not re-raise, to allow the server to start.
        # The error is logged, and subsequent API calls will show the issue.

if __name__ == '__main__':
    generate_analytics_report()
