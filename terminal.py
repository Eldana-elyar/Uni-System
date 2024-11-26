import sys
import functions_classes as fc
from colorama import Fore, Style, init

# Enable colorma
init()



def main():
    """This function is for University system main menu"""
    while True:  
        choice = input(Fore.CYAN + "\nUniversity System: (A)dmin, (S)tudent, or X: " + Style.RESET_ALL)
        match choice:
            case "A":
                admin_system()
            case "S":
                student_system()
            case "X":
                print(Fore.YELLOW + "Thank You!" + Style.RESET_ALL)
                sys.exit(1)
            case _:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)



def_admin_password = '12345'

def admin_system():
    """This function is for Admin system main menu"""
    while True: 
        choice = input(Fore.CYAN + "\n l -- Log In\n x -- Exit\nAdmin Main Menu (l/x): " + Style.RESET_ALL)
        match choice:
            case "l":
                admin_login_window()
            case "x":
                main()
            case _:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)



def admin_login_window():
    admin_password = input(Fore.GREEN + "Admin password: "+Style.RESET_ALL)

    while admin_password != def_admin_password:
            print(Fore.RED + "Incorrect password format. Please try again."+Style.RESET_ALL)
            admin_password = input(Fore.GREEN + "Admin password: "+Style.RESET_ALL)

    print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
    
    admin_window()     



def admin_window():
    """This function is for Admin system main menu"""
    while True:  
        choice = input(Fore.CYAN + "\n c -- Clear All Data\n p -- Partition Students\n g -- Grade Grouping\n r -- Remove student\n s -- Show Students Data\n x -- Exit\nAdmin system (c/p/g/r/s/x): " + Style.RESET_ALL)
        
        match choice:
            case "c":
                clear_all_data()
            case "p":
                partition_students()
            case "g":
                group_students_by_grade()    
            case "r":
                remove_student()    
            case "s":
                view_studnets()
            case "x":
                main()
            case _:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)



def view_studnets():
        students = fc.load_students()
        if students:
               print(Fore.YELLOW + "Student list:"+Style.RESET_ALL)
               for email, student in students.items():
                 print(f"ID: {student.student_id} ----> Email: {email}")
       
        else:
            print(Fore.RED + "No students registered."+Style.RESET_ALL)
        
        admin_window()     



def clear_all_data():
    students = fc.load_students()
    students.clear()
    fc.clear_all_data()
    print(Fore.RED + "Clear Data", "All student data has been cleared."+Style.RESET_ALL)
       
    admin_window()           



def partition_students():
    students = fc.load_students()
    pass_students = {}
    fail_students = {}

    for email, student in students.items():
            if student.courses:
                avg_grade = sum(int(course.mark) for course in student.courses) / len(student.courses)
                if avg_grade >= 50:
                    pass_students[email] = student
                else:
                    fail_students[email] = student

    print(Fore.YELLOW + "Partition Students - PASS/FAIL"+ Style.RESET_ALL)
    print("PASS----> ")
    for email in pass_students:
         print(f"Email: {email}, ID: {student.student_id}, Average Grade: {avg_grade}")
    print("FAIL----> ")
    for email in fail_students:
         print(f"Email: {email}, ID: {student.student_id}, Average Grade: {avg_grade}")
    
    admin_window() 



def group_students_by_grade():
    students = fc.load_students()
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
   
    print(Fore.YELLOW + "Group Students by Grade"+Style.RESET_ALL)
    for grade, group in grade_groups.items():
            print(f" {grade}  --->")
            for student in group:
                print(f"ID: {student.student_id}, Email: {student.email},Mark:{avg_grade}")

    admin_window() 



def remove_student():
        students = fc.load_students()
        id_entry = input("Enter Student ID:" )

        student_found = False  

        for email, student in list(students.items()):
            if student.student_id == id_entry:
             del students[email]
             fc.save_students(students)
             print( Fore.YELLOW + f"Student {id_entry} deleted."+Style.RESET_ALL)
             student_found = True
             break

        if not student_found:
                print(Fore.RED + "No student with that id."+Style.RESET_ALL)

        admin_window() 



def student_system():
    """This function provides options for students"""
    while True:  
        choice = input(Fore.CYAN + "\n l -- Log In\n r -- Register\n x -- Exit\nStudent System (l/r/x): " + Style.RESET_ALL)
        match choice:
            case "r":
                register_system()
            case "l":
                login_system()
            case "x":
                main()
            case _:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

    

def register_system():
    students = fc.load_students()
    print(Fore.GREEN + "Student Sign Up"+Style.RESET_ALL)
    
    while True:
        email = input(Fore.LIGHTYELLOW_EX + "Email: " + Style.RESET_ALL)
        password = input(Fore.LIGHTYELLOW_EX + "Password: " + Style.RESET_ALL)

        if not fc.is_valid_password(password) or not email.endswith("@university.com"):
            print(Fore.RED + "Incorrect email or password format. Please try again."+Style.RESET_ALL)
        else:
            # Both conditions are satisfied, exit the loop
            break
    
    while email in students:
        print(Fore.RED + "This Student is already registered."+Style.RESET_ALL)
        email = input(Fore.LIGHTYELLOW_EX+ "Email:"+Style.RESET_ALL)
        password = input(Fore.LIGHTYELLOW_EX +"Password:"+Style.RESET_ALL)

    print(Fore.YELLOW + "Email and password formats acceptable."+Style.RESET_ALL)
    print(Fore.YELLOW + f"Enrolling Student {email}."+Style.RESET_ALL)
   
    student_id = fc.generate_student_id()
    new_student = fc.Student(student_id, email, password)
    students[email] = new_student

    # Save new student
    students[new_student.email] = new_student
    # Update studens file
    fc.save_students(students)
    student_system()



def login_system():
    students = fc.load_students()
    print(Fore.GREEN + "Student Sign In" + Style.RESET_ALL)

    email = input(Fore.YELLOW + "Email: " + Style.RESET_ALL)
    password = input(Fore.YELLOW + "Password: " + Style.RESET_ALL)

    #Check email and password format
    if not fc.is_valid_password(password) or not email.endswith("@university.com"):
        print(Fore.RED + "Invalid email or password format. Please check and try again." + Style.RESET_ALL)
        student_system() 
        return  

    if email not in students:
        print(Fore.YELLOW + "Email and password formats acceptable"+ Style.RESET_ALL)
        print(Fore.RED + "Student is not registered")
        student_system() 
        return  

    while students[email].password != password:
        print(Fore.RED + "Incorrect Email or Password" + Style.RESET_ALL)
        email = input("Email: ")
        password = input("Password: ")

        
        if not fc.is_valid_password(password) or not email.endswith("@university.com"):
            print(Fore.RED + "Invalid email or password format. Please check and try again." + Style.RESET_ALL)
            student_system()  
            return  

        if email not in students:
            print(Fore.YELLOW + "Email and password formats acceptable"+ Style.RESET_ALL)
            print(Fore.RED + "Student is not registered")
            student_system()  
            return  

    print(Fore.YELLOW + "Email and password formats acceptable, Login Successful!" + Style.RESET_ALL)

    student_window(students[email])



def student_window(student):
    """
    This function displays the Student Main:
    - (s) View subjects
    - (e) Enroll in a course
    - (r) Remove a course
    - (c) Change their password
    - (x) Exit back to the student system
    """

    while True:  # Start an infinite loop
        choice = input(Fore.CYAN + "\n c -- Change password\n e -- Enroll in a Subject\n r -- Remove Subject\n s -- Show the Enrolled Subjects\n x -- Exit\n Student Course Menu (c/e/r/s/x): " + Style.RESET_ALL)
        match choice:
            case "s":
                subject_window(student)
            case "e":
                enrol_window(student)
            case "r":
                remove_subject(student)
            case "c":
                change_password(student)
            case "x":
                student_system()  
                return
            case _:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

def subject_window(student):
    if not student.courses:
        print(Fore.YELLOW + "Showing 0 subjects" + Style.RESET_ALL)
    else:
        course_count = len(student.courses)
        print(Fore.YELLOW + f"Showing {course_count} subjects" + Style.RESET_ALL)
        for idx, course in enumerate(student.courses):
            grade = fc.get_grade_letter(course.mark)
            course_info = f"[ Subject:: {course.course_id} -- mark = {course.mark} -- Grade = {grade} ]"
            print(course_info)
    
    student_window(student)



def enrol_window(student):
    students = fc.load_students()
    course_count = len(student.courses)

    if course_count < 4:
        choice = input(Fore.YELLOW + "Course Name: " + Style.RESET_ALL)
        if choice:
            for course in student.courses:
                if course.course_name == choice:
                    print(Fore.YELLOW + "You are already enrolled in this course." + Style.RESET_ALL)
                    student_window(student)
        else:
            print(Fore.RED + "Course name cannot be empty" + Style.RESET_ALL)

        course = fc.Course(choice)
        student.courses.append(course)

        subject_id = course.course_id
        
        print(Fore.YELLOW + f"Enrolling in Subject-{subject_id}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Your are now enrolled in {course_count + 1} out of 4 subjects" + Style.RESET_ALL)

        # Save new student record
        students[student.email] = student
        # Update studens file
        fc.save_students(students)
        student_window(student)
 
    else:
        print(Fore.RED + "Students are allowed to enrol in 4 subjects only." + Style.RESET_ALL)

        student_window(student)



def remove_subject(student):
    students = fc.load_students()
    subject_id = input("Remove subject by ID: ")

    found_course = None
    for course in student.courses:
        if int(course.course_id) == int(subject_id):
            found_course = course
            break

    if found_course:
        student.courses.remove(found_course)
        print(Fore.YELLOW + f"Dropping Subject-{subject_id}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"You are now enrolled in {len(student.courses)} out of 4 subjects." + Style.RESET_ALL)

        # Save new student record
        students[student.email] = student
        # Update studens file
        fc.save_students(students)
        student_window(student)

    else:
        print(Fore.RED + f"You are NOT enrolled in Subject-{subject_id}" + Style.RESET_ALL)

        student_window(student)



def change_password(student):
    students = fc.load_students()
    print(Fore.YELLOW + "Updating Password" + Style.RESET_ALL)
    new_password = input("New Password: ")
    conf_password = input("Confirm Password: ")

    while conf_password != new_password:
        print(Fore.RED + "Password does not match - try again" + Style.RESET_ALL)
        conf_password = input("Confirm Password: ")

    if not fc.is_valid_password(conf_password):
        print(Fore.RED + "Error! Invalid password format" + Style.RESET_ALL)
        change_password(student)
    else:
        student.password = conf_password
        print(Fore.GREEN + "Password has been successfully updated." + Style.RESET_ALL)

        # Save new student record
        students[student.email] = student
        # Update studens file
        fc.save_students(students)

        student_window(student)