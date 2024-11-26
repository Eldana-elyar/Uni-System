import student_window as sw
import admin_window as aw
import terminal as tm
import tkinter as tk



def main_menu():

    window = tk.Tk()
    window.title("University System Menu")

    tk.Label(window, text="Welcome to the University System").grid(row=0, column=0, columnspan=3)

    def open_admin_menu():
        window.destroy()
        aw.admin_login_window()

    def open_student_menu():
        window.destroy()
        sw.login_window()

    def exit_program():

        thank_you_label = tk.Label(window, text="Thank you", fg="red")
        thank_you_label.grid(row=2, column=1, padx=10, pady=10)
        window.after(1000, lambda: window.destroy())

    tk.Button(window, text="Admin (A)", command=open_admin_menu).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(window, text="Student (S)", command=open_student_menu).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(window, text="Exit (X)", command=exit_program).grid(row=1, column=2, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    c = input("Please select how you want to run the App: (G)GUI (T)Terminal: ")
    if c == "G":
        main_menu()
    if c == "T":
        tm.main()