# Log: Ended at counter of 5 taking a picture (Test later)
# Log2: Ended at timer for caution

# Notes:
# Average Car Length: 15-16 ft (Isuzu Taxi 14.69816 ~ 15ft)
# Average Car Movement: 25 mph = 36.67ft/s ~ 37ft/s
# Intersection at sunshine estimated longest length per lane: 22-24m ~ 23m ~ 75ft
# It takes 2.03 seconds for a 25mph vehicle to travel 75ft but will be considered as 3 seconds as it must be absolute.
# Multiply 3 seconds to the number of cars to get allotted time.
# To get stop time, add go time of next traffic light and add stop time of the succeeding lanes.

# Formulas
# Time = Distance/Speed

# ================================================================
import subprocess
import os
import smtplib
import ssl
import time
import cv2
from tkinter import *
import threading

# Global Variables
stop_threads = True
th = threading.Thread()
th.start()
th.join()

img_counter = 0
car_counter = 0
lane_counter = 0
active_light = 0
traffic_combination = 1  # Sample number of lanes (Usually 2-4)


# Camera Attribs
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap2 = cv2.VideoCapture(1)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap3 = cv2.VideoCapture(2)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap4 = cv2.VideoCapture(3)
cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap5 = cv2.VideoCapture(4)
cap5.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap5.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap6 = cv2.VideoCapture(5)
cap6.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap6.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap7 = cv2.VideoCapture(6)
cap7.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap7.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap8 = cv2.VideoCapture(7)
cap8.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap8.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap9 = cv2.VideoCapture(8)
cap9.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap9.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap10 = cv2.VideoCapture(9)
cap10.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap10.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap11 = cv2.VideoCapture(10)
cap11.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap11.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap12 = cv2.VideoCapture(11)
cap12.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap12.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cam = [cap1, cap2, cap3, cap4], \
      [cap5, cap6, cap7, cap8], \
      [cap9, cap10, cap11, cap12]


# ================ System Code ====================
def system(stop):
    global img_counter, car_counter, lane_counter, active_light, traffic_combination

    popupmsg("System Starting. . .")

    # Cascade
    car_cascade = cv2.CascadeClassifier('cascade.xml')

    def imageCaptureCount():
        global img_counter
        if img_counter != 0:
            img_name = "image_capture_" + str(img_counter) + ".png"
            cv2.imwrite(img_name, frames)
        img_counter += 1

    def activeLightChanger():
        global traffic_combination, active_light
        if active_light >= traffic_combination:
            active_light = 1
        else:
            active_light += 1
        print("===== Active Light: " + str(active_light) + " =====")

    def countdownTimerGo(t):
        while t:
            print("Time Left [Go]: " + str(t))
            time.sleep(1)
            t -= 1

    def countdownCautionCapture(t):
        global active_light
        print("Car Counted For Preceding Traffic Light: " + str(car_counter))
        while t:
            print("Time Left [Caution]: " + str(t))
            time.sleep(1)
            t -= 1

    while True:

        x = 0
        y = 0
        ret, frames = cam[x][y].read()

        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        cars = car_cascade.detectMultiScale(gray, 1.1, 2)

        for (x, y, w, h) in cars:
            cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 225), 2)

        car_counter = len(cars)

        cv2.imshow("Frame", frames)

        key = cv2.waitKey(1)

        imageCaptureCount()

        # Signal of calculation for the next traffic light
        countdownCautionCapture(5)

        # Go time for next traffic light as all other traffic lights are on stop.
        activeLightChanger()
        countdownTimerGo(3 * car_counter)
        if stop():
            break


def systemStarter():
    global stop_threads, th
    stop_threads = False
    th = threading.Thread(target=system, args=(lambda: stop_threads,))
    th.start()
    time.sleep(1)
    return stop_threads, th


def systemStopper():
    global stop_threads, th
    stop_threads = True
    th.join()
    popupmsg('System stopped.')


# ================ Functions =======================
def browseFiles():
    subprocess.Popen(r'explorer ' + os.getcwd())


def callForMaintenance():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "aislelane.cntrl@gmail.com"  # Enter your address
    receiver_email = "sammyrosecarantes@gmail.com"  # Enter receiver address
    passwordFO = "aislelane123"
    message = """From: From AisleLane <aislelane.cntrl@gmail.com>
    To: To Sammy Rose Carantes <sammyrosecarantes01@gmail.com>
    Subject: Call for Maintenance

    This is to inform you that we are currently requesting for Maintenance at our control room. Thank you!
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, passwordFO)
        server.sendmail(sender_email, receiver_email, message)
    popupmsg("Email successfully sent")


def callForFieldOps():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "aislelane.cntrl@gmail.com"  # Enter your address
    receiver_email = "sammyrosecarantes@gmail.com"  # Enter receiver address
    passwordFO = "aislelane123"
    message = """From: From AisleLane <aislelane.cntrl@gmail.com>
    To: To Sammy Rose Carantes <sammyrosecarantes@gmail.com>
    Subject: Call for Field OperatorsS

    This is to inform you that we are currently requesting for Field Operators. Please report to us as soon as you get this message. Thank you!
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, passwordFO)
        server.sendmail(sender_email, receiver_email, message)
    popupmsg("Email successfully sent")


def popupmsg(msg):
    NORM_FONT = ("Helvetica", 10)
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()
