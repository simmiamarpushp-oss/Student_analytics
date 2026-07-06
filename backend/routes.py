from flask import Blueprint, request, jsonify
import json
import os
from database import get_db_connection
from analytics import generate_analytics_report

student_routes = Blueprint('student_routes', __name__)

@student_routes.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(students)
    return jsonify({'error': 'Database connection failed'}), 500

@student_routes.route('/students/add', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    if not all([name, age, grade]):
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        val = (name, age, grade)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        try:
            generate_analytics_report()
        except Exception as e:
            print(f"Warning: analytics report update failed after adding student: {e}")
        return jsonify({'message': 'Student added successfully'}), 201
    return jsonify({'error': 'Database connection failed'}), 500


@student_routes.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM students WHERE id = %s"
        val = (student_id,)
        cursor.execute(sql, val)
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        if student:
            return jsonify(student)
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

@student_routes.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM students WHERE id = %s"
        val = (student_id,)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        try:
            generate_analytics_report()
        except Exception as e:
            print(f"Warning: analytics report update failed after deleting student: {e}")
        return jsonify({'message': 'Student deleted successfully'}), 200
    return jsonify({'error': 'Database connection failed'}), 500

@student_routes.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    if not all([name, age, grade]):
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s"
        val = (name, age, grade, student_id)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        try:
            generate_analytics_report()
        except Exception as e:
            print(f"Warning: analytics report update failed after updating student: {e}")
        return jsonify({'message': 'Student updated successfully'}), 200
    return jsonify({'error': 'Database connection failed'}), 500

@student_routes.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        # Construct path to the report file
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports', 'latest_report.json')
        with open(report_path, 'r') as f:
            report = json.load(f)
        return jsonify(report)
    except FileNotFoundError:
        return jsonify({'error': 'Analytics report not found. Generate one by sending a POST request to /api/analytics/generate.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@student_routes.route('/analytics/generate', methods=['POST'])
def generate_report():
    """
    Endpoint to trigger the generation of the analytics report.
    """
    try:
        generate_analytics_report()
        return jsonify({'message': 'Analytics report generated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to generate analytics report: {e}'}), 500
