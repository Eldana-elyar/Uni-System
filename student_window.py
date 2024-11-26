import tkinter as tk
from tkinter import messagebox
import functions_classes as fc


def login_window():
    students = fc.load_students()
    window = tk.Tk()
    window.title("The Student System")

    tk.Label(window, text="Email").grid(row=0, column=0)
    tk.Label(window, text="Password").grid(row=1, column=0)

    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1)

    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    def login():
        email = email_entry.get()
        password = password_entry.get()

        if email in students and students[email].password == password:
            messagebox.showinfo("Login", "Login Successful!")
            window.destroy()
            enrolment_window(students[email])
        else:
            messagebox.showerror("Error", "Invalid Email or Password")

    def register():
        window.destroy()
        register_window()

    def back_to_main():
        fc.return_to_main(window)

    tk.Button(window, text="Login", command=login).grid(row=2, column=0)
    tk.Button(window, text="Register", command=register).grid(row=2, column=1)
    tk.Button(window, text="Back to Main Menu", command=back_to_main).grid(row=2, column=2)

    window.mainloop()


def register_window():
    students = fc.load_students()
    window = tk.Tk()
    window.title("Register")

    tk.Label(window, text="Email").grid(row=0, column=0)
    tk.Label(window, text="Password").grid(row=1, column=0)

    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1)

    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    def register():
        email = email_entry.get()
        password = password_entry.get()

        if email in students:
            messagebox.showerror("Error", "This email is already registered.")
            return

        if not fc.is_valid_password(password):
            messagebox.showerror("Error", """Invalid password format.\n
                                 Password Requirements:
                                 - Must start with an uppercase letter
                                 - Must contain at least five letters
                                 - Must be followed by three or more digits""")
            return

        if email.endswith("@university.com"):
            student_id = fc.generate_student_id()
            new_student = fc.Student(student_id, email, password)
            students[email] = new_student
            
            # Save new student
            students[new_student.email] = new_student
            # Update studens file
            fc.save_students(students)

            messagebox.showinfo("Success", f"Registration successful! Your student ID is {student_id}")
            window.destroy()
            login_window()
        else:
            messagebox.showerror("Error", "Email must be a university email\n(@university.com)")

    tk.Button(window, text="Register", command=register).grid(row=2, column=0, columnspan=2)
    tk.Button(window, text="Return to University System", command=lambda: fc.return_to_main(window)).grid(row=3, column=0, columnspan=2)
    
    window.mainloop()


def enrolment_window(student):
    students = fc.load_students()
    window = tk.Tk()
    window.title("The Enrolment System")

    tk.Label(window, text="Course Name").grid(row=0, column=0)
    course_entry = tk.Entry(window)
    course_entry.grid(row=0, column=1)

    def enrol_course():
        if len(student.courses) >= 4:
            fc.exception_window("You cannot enroll in more than 4 courses.")
            return

        course_name = course_entry.get()
        if course_name:
            for course in student.courses:
                if course.course_name == course_name:
                    fc.exception_window("You are already enrolled in this course.")
                    return
        else:
            fc.exception_window("Course Name Cannot Be Empty")
            return

        course = fc.Course(course_name)
        student.courses.append(course)

        # Save new student record
        students[student.email] = student
        # Update studens file
        fc.save_students(students)

        total_marks = sum([int(c.mark) for c in student.courses])
        average_grade = total_marks / len(student.courses)

        messagebox.showinfo("Enrolment", f"Successfully enrolled in {course_name}! Course ID: {course.course_id}, your average grade is {average_grade:.2f}")

    tk.Button(window, text="Enroll", command=enrol_course).grid(row=1, column=0, columnspan=2)
    tk.Button(window, text="View Courses", command=lambda: subject_window(student)).grid(row=2, column=0, columnspan=2)
    tk.Button(window, text="Drop Course", command=lambda: drop_course(student)).grid(row=3, column=0, columnspan=2)
    tk.Button(window, text="Change Password", command=lambda: change_password(student)).grid(row=4, column=0, columnspan=2)
    tk.Button(window, text="Logout", command=lambda: fc.return_to_main(window)).grid(row=5, column=0, columnspan=2)
    window.mainloop()

def subject_window(student):
    window = tk.Tk()
    window.title("Enrolled Subjects")

    if not student.courses:
        tk.Label(window, text="You are not enrolled in any courses.").grid(row=0, column=0)
    else:
        for idx, course in enumerate(student.courses):
            grade = fc.get_grade_letter(course.mark)
            course_info = f"Course: {course.course_name}, ID: {course.course_id}, Mark: {course.mark}, Grade: {grade}"
            tk.Label(window, text=course_info).grid(row=idx, column=0)

    window.mainloop()

def drop_course(student):
    students = fc.load_students()
    window = tk.Tk()
    window.title("Drop Course")

    tk.Label(window, text="Course ID").grid(row=0, column=0)
    course_entry = tk.Entry(window)
    course_entry.grid(row=0, column=1)

    def confirm_drop():
        entered_course_id = course_entry.get()
        for course in student.courses:
            if int(course.course_id) == int(entered_course_id):
                student.courses.remove(course)

                # Save new student record
                students[student.email] = student
                # Update studens file
                fc.save_students(students)
                messagebox.showinfo("Drop Course", f"You have successfully dropped {entered_course_id}.")
                break
                
            else:
                messagebox.showinfo("Drop Course", f"Course {entered_course_id} Not Enrolled.")

        window.destroy()

    tk.Button(window, text="Drop", command=confirm_drop).grid(row=1, column=0, columnspan=2)

    window.mainloop()


def change_password(student):
    students = fc.load_students()
    window = tk.Tk()
    window.title("Change Password")

    tk.Label(window, text="New Password").grid(row=0, column=0)
    new_password_entry = tk.Entry(window, show="*")
    new_password_entry.grid(row=0, column=1)

    def confirm_change():
        new_password = new_password_entry.get()
        if not fc.is_valid_password(new_password):
            messagebox.showerror("Error", "Invalid password format.")
        else:
            student.password = new_password

            # Save new student record
            students[student.email] = student
            # Update studens file
            fc.save_students(students)

            messagebox.showinfo("Change Password", "Password successfully changed.")
        window.destroy()

    tk.Button(window, text="Change", command=confirm_change).grid(row=1, column=0, columnspan=2)

    window.mainloop()
