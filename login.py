from GUI import *

from PIL import Image, ImageTk

from functools import partial


# =================== Login ====================
def validateLogin(username, password):
    user = username.get()
    userPass = password.get()
    if user == "admin" and userPass == "pass":
        login_main.withdraw()
        aisleLane()
    else:
        popupmsg("Incorrect Username and Password")


# =================== GUI Login ===================

# window
login_main = Tk()
login_main.geometry('1366x720')
login_main.title('Login')
loginbg = Image.open('bgimg.png')
bgimg = ImageTk.PhotoImage(loginbg)
login_mainbg = Label(image=bgimg)
login_mainbg.image = bgimg
login_mainbg.place(x=0, y=0, relwidth=1, relheight=1)

# username label and text entry box
usernameLabel = Label(login_main, text="Username:").place(x=260, y=340)
username = StringVar()
usernameEntry = Entry(login_main, textvariable=username, width=28).place(x=260, y=370)

# password label and password entry box
passwordLabel = Label(login_main, text="Password:").place(x=260, y=400)
password = StringVar()
passwordEntry = Entry(login_main, textvariable=password, show='*', width=28).place(x=260, y=430)

validateLogin = partial(validateLogin, username, password)

# login button
loginButton = Button(login_main, text="Login", command=validateLogin).place(x=260, y=460)


# =================== Popup =====================
def popupmsg(msg):
    NORM_FONT = ("Helvetica", 10)
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()
