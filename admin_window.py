import tkinter as tk
from tkinter import messagebox
import functions_classes as fc

admin_password = '12345'


def admin_login_window():
    window = tk.Tk()
    window.title("Admin Login")

    tk.Label(window, text="Admin Password:").grid(row=0, column=0)

    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=0, column=1)

    def admin_login():
        if password_entry.get() == admin_password:
            messagebox.showinfo("Login", "Admin Login Successful!")
            window.destroy()
            admin_menu_window()
            print("togra")
        else:
            messagebox.showerror("Error", "Invalid Admin Password")
            print("hata")

    tk.Button(window, text="Login", command=admin_login).grid(row=1, column=0, columnspan=2)
    tk.Button(window, text="Return to Main Menu", command=lambda: fc.return_to_main(window)).grid(row=2, column=0, columnspan=2)

    window.mainloop()

def admin_menu_window():
    students = fc.load_students()
    window = tk.Tk()
    window.title("Admin Menu")
    window.geometry("400x300")

    def view_students():
        view_window = tk.Tk()
        view_window.title("All Students")
        if students:
            for email, student in students.items():
                student_info = f"ID: {student.student_id}, Email: {email}, Courses: {len(student.courses)}, Course IDs: "
                student_info += ", ".join([str(course.course_id) for course in student.courses])
                tk.Label(view_window, text=student_info).pack()
        else:
            tk.Label(view_window, text="No students registered.").pack()

    def delete_student():
        delete_window = tk.Tk()
        delete_window.title("Delete Student")

        tk.Label(delete_window, text="Enter Student ID:").grid(row=0, column=0)
        id_entry = tk.Entry(delete_window)
        id_entry.grid(row=0, column=1)

        def delete():
            student_id = id_entry.get()
            for email, student in students.items():
                if student.student_id == student_id:
                    del students[email]
                    fc.save_students(students)
                    messagebox.showinfo("Delete", f"Student {student_id} deleted.")
                    delete_window.destroy()
                    break
            else:
                messagebox.showerror("Error", "No student with that id.")

        tk.Button(delete_window, text="Delete", command=delete).grid(row=1, column=0, columnspan=2)

    def partition_students():
        pass_students = {}
        fail_students = {}

        for email, student in students.items():
            if student.courses:
                avg_grade = sum(int(course.mark) for course in student.courses) / len(student.courses)
                if avg_grade >= 50:
                    pass_students[email] = student
                else:
                    fail_students[email] = student
            else:
                fail_students[email] = student

        partition_window = tk.Tk()
        partition_window.title("Partition Students - PASS/FAIL")

        tk.Label(partition_window, text="PASS Students:").pack()
        for email in pass_students:
            tk.Label(partition_window, text=email).pack()

        tk.Label(partition_window, text="FAIL Students:").pack()
        for email in fail_students:
            tk.Label(partition_window, text=email).pack()


    def group_students_by_grade():
        grade_groups = {
            "HD": [], "D": [], "C": [], "P": [], "Z": []
        }
        for student in students.values():
            avg_grade = sum(int(course.mark) for course in student.courses) / len(student.courses) if student.courses else 0
            if avg_grade >= 85:
                grade_groups["HD"].append(student)
            elif avg_grade >= 75:
                grade_groups["D"].append(student)
            elif avg_grade >= 65:
                grade_groups["C"].append(student)
            elif avg_grade >= 50:
                grade_groups["P"].append(student)
            else:
                grade_groups["Z"].append(student)

        group_window = tk.Tk()
        group_window.title("Group Students by Grade")

        for grade, group in grade_groups.items():
            tk.Label(group_window, text=f"Grade {grade} Students:").pack()
            for student in group:
                tk.Label(group_window, text=f"ID: {student.student_id}, Email: {student.email}").pack()
    

    def clear_all_data():
        confirm = messagebox.askyesno("Clear All Data", "Are you sure you want to delete all student data?")
        if confirm:
            students.clear()
            fc.clear_all_data()
            messagebox.showinfo("Clear Data", "All student data has been cleared.")

    tk.Button(window, text="View Students", command=view_students).grid(row=0, column=0, sticky="ew")
    tk.Button(window, text="Delete Student", command=delete_student).grid(row=1, column=0, sticky="ew")
    tk.Button(window, text="Partition Students (PASS/FAIL)", command=partition_students).grid(row=2, column=0, sticky="ew")
    tk.Button(window, text="Group Students by Grade", command=group_students_by_grade).grid(row=3, column=0, sticky="ew")
    tk.Button(window, text="Clear All Data", command=clear_all_data).grid(row=4, column=0, sticky="ew")
    tk.Button(window, text="Logout", command=lambda: fc.return_to_main(window)).grid(row=5, column=0, sticky="ew")

    window.mainloop()