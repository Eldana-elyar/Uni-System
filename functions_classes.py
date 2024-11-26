import json
import random
import os
from tkinter import messagebox
import re
import app 
import tkinter as tk


STUDENT_FILE = 'students.json'
admin_password = "12345"

# Initialize the JSON file for students if it does not exist
if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, 'w') as f:
        pass       # Create the file without writing any content
    print("students.json created successfully.")
else:
    print("students.json exists. Loading students from file...")

class Student:
    used_student_ids = set()

    def __init__(self, student_id, email, password):
        self.student_id = student_id
        self.email = email
        self.password = password
        self.courses = []

        # Add student ID to the set to avoid duplicates
        Student.used_student_ids.add(student_id)

class Course:
    course_ids = {}
    course_id_file = "courses.json"

    def __init__(self, course_name, course_id=None, mark=None):
        self.course_name = course_name
        self.load_course_ids()  # Load existing course IDs at initialization
        self.course_id = course_id if course_id else self.get_or_generate_course_id()
        self.mark = mark if mark else self.assign_mark()

    @classmethod
    def load_course_ids(cls):
        """Load course IDs from a JSON file."""
        if os.path.exists(cls.course_id_file):
            with open(cls.course_id_file, 'r') as f:
                cls.course_ids = json.load(f)
        else:
            cls.course_ids = {}  # Initialize to an empty dictionary if file doesn't exist

    @classmethod
    def save_course_ids(cls):
        """Save course IDs to a JSON file."""
        with open(cls.course_id_file, 'w') as f:
            json.dump(cls.course_ids, f)

    def get_or_generate_course_id(self):
        """Get or generate a course ID based on the course name."""
        if self.course_name in Course.course_ids:
            return Course.course_ids[self.course_name]
        else:
            new_id = random.randint(1, 999)
            formatted_number = str(new_id).zfill(3)
            Course.course_ids[self.course_name] = new_id
            Course.save_course_ids()    # Save updated IDs
            return formatted_number

    def assign_mark(self):
        """Assign a random mark between 25 and 100."""
        return random.randint(25, 100)


def load_students():
    """Load students dictionary from the JSON file."""
    students = {}
    try:
        with open(STUDENT_FILE, 'r') as f:
            data = json.load(f)
            for email, student_data in data.items():
                student_id = student_data['student_id']
                password = student_data['password']
                courses = [Course(course['course_name'], course['course_id'], course['mark']) for course in student_data['courses']]
                
                student = Student(student_id, email, password)
                student.courses = courses
                students[email] = student
    except json.JSONDecodeError as error:
        print("Database Empty", "No students in the database yet. Please register first.")
    return students

def is_valid_password(password):
    return re.match(r'^(?=.*[A-Z])[a-zA-Z]{5,}\d{3,}$', password) is not None

def generate_student_id():
    student_id = random.randint(1, 999999)
    formatted_student_id = str(student_id).zfill(6)
    while formatted_student_id in Student.used_student_ids:
        student_id = random.randint(1, 999999)
        formatted_student_id = str(student_id).zfill(6)

    Student.used_student_ids.add(formatted_student_id)
    return formatted_student_id

def save_students(students):
    """Save students dictionary to the JSON file."""

    data = {
        email: {
            'student_id': student.student_id,
            'password': student.password,
            'courses': [{'course_name': course.course_name, 'course_id': course.course_id, 'mark': course.mark} for course in student.courses]
        } for email, student in students.items()
    }
    with open(STUDENT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def return_to_main(window):
    window.destroy()
    app.main_menu()

def exception_window(message):
    window = tk.Tk()
    window.title("Error")

    tk.Label(window, text=message).grid(row=0, column=0)
    tk.Button(window, text="OK", command=window.destroy).grid(row=1, column=0)

    window.mainloop()

def get_grade_letter(mark):
    mark = int(mark)
    if mark < 50:
        return "Z"
    elif mark < 65:
        return "P"
    elif mark < 75:
        return "C"
    elif mark < 85:
        return "D"
    else:
        return "HD" 

def clear_all_data():
    with open(STUDENT_FILE, "w") as file:
        json.dump({}, file)