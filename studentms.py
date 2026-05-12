from tkinter import *
from tkinter import messagebox, ttk

top = Tk()
top.geometry("400x350")
top.title("Login System")


def show_register():
    login_frame.pack_forget()
    register_frame.pack()

def show_login():
    register_frame.pack_forget()
    login_frame.pack()


def register():
    uname = reg_user.get()
    email = reg_email.get()
    passw = reg_pass.get()
    cpass = reg_cpass.get()

    if uname == "" or email == "" or passw == "" or cpass == "":
        messagebox.showerror("Error", "All fields are required.")
        return

    if passw != cpass:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    
    
    with open("users.txt", "r") as file:
        for line in file:
            try:
                stored_uname, stored_email, _ = line.strip().split(", ")
            except ValueError:
                continue  # skip invalid lines

        if uname == stored_uname:
            messagebox.showerror("Error", "Username already registered")
            return
        
        if email == stored_email:
            messagebox.showerror("Error", "Email already registered")
            return

    with open("users.txt", "a") as file:
        file.write(f"{uname}, {email}, {passw}\n")

    messagebox.showinfo("Success", "Registration successful")

    reg_user.delete(0, END)
    reg_email.delete(0, END)
    reg_pass.delete(0, END)
    reg_cpass.delete(0, END)
    show_login()
    
def open_home():
    uname = login_user.get()

    home = Toplevel(top)
    home.title("Home Page")
    home.geometry("800x650")

    def on_closing():
        if messagebox.askyesno("Exit", "Are you sure you want to close?"):
            home.destroy()

    home.protocol("WM_DELETE_WINDOW", on_closing)

    Label(home, text="Student Information System", font=("Arial", 13, "bold")).pack(pady=10)
    Label(home, text=f"Welcome {uname}!", font=("Arial", 11)).pack(pady=10)

    form_frame = Frame(home)
    form_frame.pack(pady=10)

    Label(form_frame, text='Student ID').grid(row=0, column=0, pady=5)
    entry_sid = Entry(form_frame)
    entry_sid.grid(row=0, column=1, pady=5)

    Label(form_frame, text='Name').grid(row=1, column=0, pady=5)
    entry_name = Entry(form_frame)
    entry_name.grid(row=1, column=1, pady=5)

    Label(form_frame, text="Course").grid(row=2, column=0, pady=5)
    combo_course = ttk.Combobox(form_frame, values=["BSIT", "BSCS", "BSCpE"], state="readonly")
    combo_course.grid(row=2, column=1, pady=5)

    Label(form_frame, text="Year").grid(row=3, column=0, pady=5)
    combo_year = ttk.Combobox(form_frame, values=["1ST", "2ND", "3RD", "4TH"], state="readonly")
    combo_year.grid(row=3, column=1, pady=5)

    Label(form_frame, text="Gender").grid(row=4, column=0, pady=5)
    gender_var = StringVar(value="none")
    Radiobutton(form_frame, text="Male", variable=gender_var, value="Male").grid(row=4, column=1, pady=5)
    Radiobutton(form_frame, text="Female", variable=gender_var, value="Female").grid(row=4, column=2, pady=5)

    scholar_var = IntVar()
    Checkbutton(form_frame, text="Scholar", variable=scholar_var).grid(row=5, column=1, pady=5)

    table_frame = Frame(home)
    table_frame.pack(pady=10)

    columns = ("Student ID", "Name", "Course", "Year", "Gender", "Scholar")
    student_table = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        student_table.heading(col, text=col)
        student_table.column(col, width=110)

    student_table.pack()

    def clear_fields():
        entry_sid.delete(0, END)
        entry_name.delete(0, END)
        combo_course.set("")
        combo_year.set("")
        gender_var.set("none")
        scholar_var.set(0)

    def load_data():
        try:
            with open("students.txt", "r") as file:
                for line in file:
                    data = line.strip().split(", ")
                    student_table.insert("", END, values=data)
        except FileNotFoundError:
            pass

    def insert_data():
        sid = entry_sid.get()
        name = entry_name.get()
        course = combo_course.get()
        year = combo_year.get()
        gender = gender_var.get()
        scholar = "Yes" if scholar_var.get() else "No"

        if sid == "" or name == "" or course == "" or year == "":
            messagebox.showerror("Error", "All fields required")
            return

        if gender == "none":
            messagebox.showerror("Error", "Select gender")
            return

        for row in student_table.get_children():
            if student_table.item(row)['values'][0] == sid:
                messagebox.showerror("Error", "Student ID already exists")
                return

        with open("students.txt", "a") as file:
            file.write(f"{sid}, {name}, {course}, {year}, {gender}, {scholar}\n")

        student_table.insert("", END, values=(sid, name, course, year, gender, scholar))
        messagebox.showinfo("Success", "Student Added")
        clear_fields()

    def delete_data():
        selected = student_table.selection()

        if not selected:
            messagebox.showerror("Error", "Select a student first")
            return

        confirm = messagebox.askyesno("Delete", "Delete selected student?")
        if confirm:
            for item in selected:
                student_table.delete(item)

            with open("students.txt", "w") as file:
                for row in student_table.get_children():
                    data = student_table.item(row)['values']
                    file.write(", ".join(data) + "\n")
    
    
    #local variable
    #bakit ailangan may variable sa labas
    #
    editing = False 
    selected_item = None

    def update_after_edit():
        with open("student.txt", "w") as file:
            for row in student_table.get_children(): #row-hori col-vert
                values = student_table.items(row, "values")
                file.write(", ".join(values) + "\n")


    def edit_student():
        nonlocal editing, selected_item #they will share the variable outside

        #edit mode1
        if not editing:
            selected_item = student_table.focus()

            if not selected_item:
                messagebox.showerror("Error", "Please select a record to edit.")
                return
            
            values = student_table.item(selected_item, "values") #return of list of data (e.g. sid, courrse, year, gender etc.)

            clear_fields()
            entry_sid.insert(0, values[0])
            entry_name.insert(0, values[1])
            combo_course.set(values[2])
            combo_year.set(values[3])
            gender_var.set(values[4])
            scholar_var.set(1 if values[5] == "Yes" else 0)

            #change state
                     
            editing = True
            entry_sid.config(state="readonly")
            edit_btn.config(text="Update")
            add_btn.config(state="disabled")
            delete_btn.config(state="disabled")

    

        else:
            sid = entry_sid.get()
            name = entry_name.get()
            course = combo_course.get()
            year = combo_year.get()
            gender = gender_var.get()
            scholar = "Yes" if scholar_var.get() else "No"

            if sid == "" or name == "" or course == "" or year == "":
                messagebox.showerror("Error", "All fields required")
                return

            if gender == "none":
                messagebox.showerror("Error", "Select gender")
                return

            student_table.item(selected_item,values=(sid, name, course,
                                        year, gender, scholar))

            #update_after_edit()
            messagebox.showinfo("Update Student", "Student record updated successfully.")


            with open("students.txt", "w") as file:
                for row in student_table.get_children():
                    data = student_table.item(row)['values']
                    file.write(", ".join(data) + "\n")

            messagebox.showinfo("Update Student", "Student record updated successfully.")

            edit_btn.config(text="Edit Student")
            add_btn.config(state="normal")
            delete_btn.config(state="normal")
            editing = False
            clear_fields()

    btn_frame = Frame(home)
    btn_frame.pack(pady=5)

    add_btn = Button(btn_frame, text="Add Student", bg="green", fg="white", width=15,
                     command=insert_data)
    add_btn.grid(row=0, column=0, padx=10)

    delete_btn = Button(btn_frame, text="Delete Student", bg="red", fg="white", width=15,
                        command=delete_data)
    delete_btn.grid(row=0, column=1, padx=10)

    edit_btn = Button(btn_frame, text="Edit Student", bg="yellow", fg="white", width=15,
                      command=edit_student)
    edit_btn.grid(row=0, column=2, padx=10)

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            home.destroy()

    Button(home, text="Logout", bg="red", fg="white", command=logout, width=10).pack(pady=15)

    load_data()



login_frame = Frame(top)

Label(login_frame, text="Login Form", font=("arial", 16, "bold")).pack(pady=10)

Label(login_frame, text="Username").pack(pady=3)
login_user = Entry(login_frame)
login_user.pack(pady=5)

Label(login_frame, text="Password").pack(pady=3)
login_pass = Entry(login_frame, show="*")
login_pass.pack(pady=5)

Button(login_frame, text="Login", bg="green", fg="white", width=10,
       command=open_home).pack(pady=10)

Button(login_frame, text="Register", bg="blue", fg="white", width=10,
       command=show_register).pack(pady=5)


register_frame = Frame(top)

Label(register_frame, text="Registration Form").pack(pady=10)

Label(register_frame, text="Username").pack(pady=3)
reg_user = Entry(register_frame)
reg_user.pack(pady=5)

Label(register_frame, text="E-mail").pack(pady=3)
reg_email = Entry(register_frame)
reg_email.pack(pady=5)

Label(register_frame, text="Password").pack(pady=3)
reg_pass = Entry(register_frame, show="*")
reg_pass.pack(pady=5)

Label(register_frame, text="Confirm Password").pack(pady=3)
reg_cpass = Entry(register_frame, show="*")
reg_cpass.pack(pady=5)

Button(register_frame, text="Register", command=register, width=10).pack(pady=10)
Button(register_frame, text="Back", command=show_login).pack(pady=5)

login_frame.pack()

top.mainloop()