# University System
 This is an University System that provides both a CLI and a GUI for user interaction.

## How to Run
Open the `Uni_System2024` folder and then run the `app.py` file inside. You can choose between the two modes:
- Enter `G` to launch the GUI.
- Enter `T` to launch the CLI for interacting with the system via the terminal.

## Note: 
1.Ensure `colorama` is installed by running `pip install colorama` if needed.
2.Ensure you have the latest version of Python installed.

## Features
The University System includes two subsystems: Student and Admin.

### Student System
The student system provides students with the following capabilities:
- **Register and Login**: Students can create an account and log in.
- **Enroll in Courses**: Students can enroll in a maximum of 4 courses.
- **Show the Courses**: Show the enrolled subjects with their marks and grades.
- **Remove Courses**: Students can remove courses they've enrolled in.
- **Change Password**: Students can update their account password.

### Admin System
The Admin password is`12345`. 
The admin system enables administrators to perform the following actions:
- **Clear the Database**: Deletes all student data from the system.
- **View All Students**: Displays a list of all registered students.
- **Group Students by Grade**: Groups students based on their average grade.
- **Categorize Students by Pass/Fail**: Classifies students based on whether they passed or failed.
- **Remove Student by ID**: Deletes a specific student by their ID.
