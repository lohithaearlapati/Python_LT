from tkinter import Label, Tk, Frame, Button, Entry, messagebox, Toplevel
from mysql.connector import connect
import re

conn = connect(
    host='localhost',
    user='root',
    password='Veneela@555',
    database='demo'
)
cur = conn.cursor()

font = ('Courier New', 20, 'bold italic')


class Home:
    def __init__(self, root) -> None:
        self.root = root
        self.main_frame = Frame(self.root, width=550, height=350, bg='black')
        self.main_frame.place(x=0, y=0)
        self.name_lbl = Label(self.main_frame, text="USER NAME", font=font, width=10)
        self.name_lbl.place(x=10, y=50)
        self.name_entry = Entry(self.main_frame, font=font, width=15)
        self.name_entry.place(x=230, y=50)

        self.pass_lbl = Label(self.main_frame, text='PASSWORD', font=font, width=10)
        self.pass_lbl.place(x=10, y=150)
        self.pass_entry = Entry(self.main_frame, font=font, width=15)
        self.pass_entry.place(x=230, y=150)

        self.login_btn = Button(self.main_frame, text='LOGIN', font=font, width=10, command=self.login_fun)
        self.login_btn.place(x=200, y=240)

        self.forgot_password_btn = Button(self.main_frame, text='Forgot Password', font=('Courier New', 10, 'bold'),
                                          command=self.forgot_password)
        self.forgot_password_btn.place(x=5, y=300)

        self.goto_register = Label(self.main_frame, text='NOT A MEMBER YET? SIGNUP!',
                                   font=('Courier New', 10, 'bold'))
        self.goto_register.place(x=320, y=300)
        self.goto_register.bind("<Button-1>", self.change_page)

    def change_page(self, event):
        self.main_frame.destroy()
        register = Register(root)

    def login_fun(self):
        self.user_name = self.name_entry.get()
        self.user_pass = self.pass_entry.get()

        cur.execute('select * from user_details')
        self.name_pool = cur.fetchall()
        self.name_pool = [item[1] for item in self.name_pool]

        if self.user_name in self.name_pool:
            cur.execute(f'select Roll from user_details where Name = "{self.user_name}"')
            self.roll = cur.fetchall()
            self.roll = [item[0] for item in self.roll]
            if self.user_pass in self.roll:
                messagebox.showinfo('YAY', 'LOGED IN')
                import translator

    def forgot_password(self):
        self.reset_window = Toplevel(root)
        self.reset_window.title('Reset Password')
        self.reset_window.geometry('500x200')
        self.reset_window.resizable(False, False)
        self.reset_window.configure(bg='black') 

        self.reset_name_lbl = Label(self.reset_window, text='UserName', font=font)
        self.reset_name_lbl.place(x=20, y=30)

        space_lbl = Label(self.reset_window, text='', bg='black')
        space_lbl.place(x=0, y=50)  # Adjust the position to control the space

        self.reset_name_entry = Entry(self.reset_window, font=font, width=15)
        self.reset_name_entry.place(x=200, y=30)

        self.reset_pass_lbl = Label(self.reset_window, text='Password', font=font)
        self.reset_pass_lbl.place(x=20, y=80)
        self.reset_pass_entry = Entry(self.reset_window, font=font, width=15)
        self.reset_pass_entry.place(x=200, y=80)

        self.reset_btn = Button(self.reset_window, text='Reset Password', font=font, width=15,
                                command=self.reset_password)
        self.reset_btn.place(x=150, y=130)

        

    def reset_password(self):
        reset_username = self.reset_name_entry.get()
        reset_password = self.reset_pass_entry.get()

        if reset_username and reset_password:
            cur.execute(f'UPDATE user_details SET Roll = "{reset_password}" WHERE Name = "{reset_username}"')
            conn.commit()
            messagebox.showinfo('Success', 'Password reset successful')
            self.reset_window.destroy()
        else:
            messagebox.showerror('Error', 'Please enter username and new password')


class Register:
    def __init__(self, root) -> None:
        self.root = root
        self.main_frame = Frame(self.root, width=550, height=350, bg='black')
        self.main_frame.place(x=0, y=0)

        self.name_lbl = Label(self.main_frame, text="USER NAME", font=font, width=10)
        self.name_lbl.place(x=10, y=50)
        self.name_entry = Entry(self.main_frame, font=font, width=15)
        self.name_entry.place(x=230, y=50)

        self.pass_lbl = Label(self.main_frame, text='PHONE NO', font=font, width=10)
        self.pass_lbl.place(x=10, y=100)
        self.pass_entry = Entry(self.main_frame, font=font, width=15)
        self.pass_entry.place(x=230, y=100)

        self.roll_lbl = Label(self.main_frame, text='PASSWORD', font=font, width=10)
        self.roll_lbl.place(x=10, y=150)
        self.roll_entry = Entry(self.main_frame, font=font, width=15)
        self.roll_entry.place(x=230, y=150)
        

        self.register_btn = Button(self.main_frame, text='REGISTER', font=font, width=10, command=self.register_user)
        self.register_btn.place(x=200, y=240)

        self.goto_register = Label(self.main_frame, text='Already a member? login!',
                                   font=('Courier New', 10, 'bold'))
        self.goto_register.place(x=5, y=300)
        self.goto_register.bind("<Button-1>", self.change_page)

    def register_user(self):
        self.name = self.name_entry.get()
        self.roll = self.roll_entry.get()
        self.dept = self.pass_entry.get()

        # Check if the department already exists for any user
        cur.execute('SELECT * FROM user_details WHERE Dept = %s', (self.dept,))
        existing_users = cur.fetchall()

        if existing_users:
            messagebox.showerror('Error', 'User already exists!')
            return


        if not re.match("^[A-Za-z]+$", self.name):
            messagebox.showerror('Error', 'Username must contain only alphabets')
            return

        self.query = 'insert into user_details (Roll, Name, Dept) values(%s,%s,%s)'
        self.values = (self.roll, self.name, self.dept)
        cur.execute(self.query, self.values)
        conn.commit()
        messagebox.showinfo('registered', 'you are registered')

    def change_page(self, event):
        self.main_frame.destroy()
        home = Home(root)


root = Tk()
root.title('DEMO')
root.geometry('550x350+550+200')
root.resizable(False, False)
home = Home(root)
root.mainloop()
