from tkinter import *

top = Tk()
top.title("Login Page")
top.geometry("400x350")

Label(top, text="Login Form", font="bold").pack(pady=25)

Label(top, text="Username").pack(pady=5)
entry_username = Entry(top, width=30).pack()


Label(top, text="Password").pack(pady=5)
entry_password = Entry(top, width=30, show="*").pack()


Button(top, text="Login", bg="green", fg="white", command=home).pack(pady=20)
Button(top, text="Register", bg="blue", fg="white", command=register).pack(pady=2)

top.mainloop()