from system import *
from PIL import Image, ImageTk

import threading


# ================ GUI Code =======================
def aisleLane():
    master = Toplevel()
    master.title("AisleLane")
    menu = Menu(master)
    master.config(menu=menu)
    master.geometry("1366x720")

    # Background Image
    guibg = Image.open('aislelanebg.png')
    guiimg = ImageTk.PhotoImage(guibg)
    masterbg = Label(master, image=guiimg)
    masterbg.image = guiimg
    masterbg.place(x=0, y=0, relwidth=1, relheight=1)

    # Camera
    lmain = Label(master)
    lmain.place(x=387, y=14)

    def show_frame1():
        _, frame = cap1.read()
        frame = cv2.resize(frame, (472, 338))
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame1)

    # Menus
    fileMenu = Menu(menu)
    menu.add_cascade(label='File', menu=fileMenu)
    fileMenu.add_command(label='-----')
    editMenu = Menu(menu)
    menu.add_cascade(label='Edit', menu=editMenu)
    editMenu.add_command(label='-----')
    viewMenu = Menu(menu)
    menu.add_cascade(label='View', menu=viewMenu)
    viewMenu.add_command(label='-----')
    toolsMenu = Menu(menu)
    menu.add_cascade(label='Tools', menu=toolsMenu)
    toolsMenu.add_command(label='-----')
    settingsMenu = Menu(menu)
    menu.add_cascade(label='Settings', menu=settingsMenu)
    settingsMenu.add_command(label='-----')

    # Dropdown
    locnum = {'Location 1'}
    locnum = sorted(locnum)
    locno = StringVar(master)
    locno.set('Location 1')

    locPopUp = OptionMenu(master, locno, *locnum)
    Label(master, text="Location:").place(x=30, y=150)
    locPopUp.place(x=25, y=175)

    def change_dropdownloc():
        if locno.get() == "Location 1":
            print(locno.get())

    locno.trace('w', change_dropdownloc)

    # Threading

    # Buttons
    buttonFiles = Button(master, text="Open Files", command=browseFiles, height=2, width=8)
    buttonStart = Button(master, text="System Start", command=systemStarter, height=2)
    buttonStop = Button(master, text="System Stop", command=systemStopper, height=2)
    buttonMaintenance = Button(master, text="Call for Maintenance", command=callForMaintenance, height=2)
    buttonField = Button(master, text="Call for Field Operator", command=callForFieldOps, height=2)
    buttonExit = Button(master, text="Exit", command=exit, height=2, width=8)
    buttonFiles.place(x=160, y=260)
    buttonStart.place(x=25, y=310)
    buttonStop.place(x=280, y=310)
    buttonMaintenance.place(x=25, y=380)
    buttonField.place(x=230, y=380)
    buttonExit.place(x=160, y=440)

    threading.Thread(target=show_frame1())

    mainloop()
