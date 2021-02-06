import tkinter as tk
from tkinter.messagebox import showinfo
from ping3 import ping
from json import load
from os import listdir
from sys import exit


def createSetting():    # to create setting.json
    import json
    datas = {}
    datas["ping1"] = "8.8.8.8"
    datas["ping2"] = "192.168.100.1"
    datas["xpos"] = "10"
    datas["ypos"] = "30"
    datas["text1"] = "Google"
    datas["text2"] = "Router"
    datas["rightClick"] = True

    with open('setting.json', 'w') as default:
        json.dump(datas, default)


def preCheckSetting():  # function to check setting.json file
    hasSettingsJson = False
    for i in listdir("."):
        if "setting.json" in i:
            hasSettingsJson = True
    if not hasSettingsJson:
        createSetting()


def getSetting(filename):
    with open(filename, "r") as f:
        my_dict = load(f)
    return my_dict


preCheckSetting()
settingsPath = "setting.json"

# Set global variables
datas = getSetting(settingsPath)
target1 = datas["ping1"]
target2 = datas["ping2"]
xpos = datas["xpos"]
ypos = datas["ypos"]
label1Text = datas["text1"]
label2Text = datas["text2"]
rightClickInfo = datas["rightClick"]

windowSize = "100x40"  # constant window size
geometry = windowSize + "+" + xpos + "+" + ypos


def checkPingAvg(target, count=10): # check average ping by testing n-times
    total = 0
    for i in range(count):
        a = ping(target, unit="ms", size=10)
        try:
            a = int(a)
        except:
            if a is None:
                return int(-1)  # For future application, no use yet.
            else:
                return int(-2)  # For future application, no use yet.
        total = a + total
    total = total / count
    return total


window = tk.Tk()
window.title("PingStat")

window.geometry(geometry)
window.columnconfigure([0, 1], minsize=50)
window.rowconfigure(0, minsize=0)


def scanning():
    window.lift() # Lift app to always show on top.
    pingA = checkPingAvg(target1)
    ping1['text'] = pingA # set ping to be displayed
    pingB = checkPingAvg(target2)
    ping2['text'] = pingB # set ping to be displayed

    # Simple if state...
    if pingA < 0:
        ping1['background'] = "gray50"
    else:
        if pingA <= 50:
            ping1['background'] = "green yellow"
            ping1['foreground'] = 'black'
        elif pingA <= 100:
            ping1['background'] = "dark green"
            ping1['foreground'] = 'white'
        elif pingA <= 200:
            ping1['background'] = "yellow"
            ping1['foreground'] = 'black'
        else:
            ping1['background'] = "red"
            ping1['foreground'] = 'white'

    if pingB < 0:
        ping2['background'] = "gray50"
    else:
        if pingB <= 50:
            ping2['background'] = "green yellow"
            ping2['foreground'] = 'black'
        elif pingB <= 100:
            ping2['background'] = "dark green"
            ping2['foreground'] = 'white'
        elif pingB <= 200:
            ping2['background'] = "yellow"
            ping2['foreground'] = 'black'
        else:
            ping2['background'] = "red"
            ping2['foreground'] = 'white'

    # After 0.5 second, call scanning again (create a recursive loop)
    window.after(500, scanning)


def closeSequence(event):
    exit()


def showCredits(event):
    showinfo("Credits", "To disable Right Click, edit setting.json\n"
                        "and change 'rightclick' to false\n"
                        "By Faiz Noerdiyan Cesara \n"
                        "Mail me at faiznc@gmail.com")


def changeOnHovering(event):
    window.wm_attributes("-alpha", 1)


def returnToNormalState(event):
    window.wm_attributes("-alpha", 0.5)


def rightClick(event):
    if rightClickInfo:
        showinfo("Info", "Ctrl+F5 to close\nF11 for more info")


ping1 = tk.Label(text="0", background="gray50", border=0, padx=3, relief="solid", borderwidth=1, width=5,
                 foreground="white")
ping1.grid(row=0, column=0)

ping2 = tk.Label(text="0", background="gray50", border=0, padx=3, relief="solid", borderwidth=1, width=5,
                 foreground="white")
ping2.grid(row=0, column=1)

label1 = tk.Label(text=label1Text, width=5)
label1.config(font=("Times New Roman", 6))
label1.grid(row=1, column=0, sticky="N")

label2 = tk.Label(text=label2Text, width=5)
label2.config(font=("Times New Roman", 6))
label2.grid(row=1, column=1, sticky="N")

window.bind('<Control-F5>', closeSequence)
window.bind('<F11>', showCredits)

window.bind('<Enter>', changeOnHovering)
window.bind('<Leave>', returnToNormalState)

window.bind("<Button-2>", rightClick)
window.bind("<Button-3>", rightClick)

window.after(100, scanning)  # To automatically run ping test
window.attributes('-topmost', True)  # Always on top of another windows
window.overrideredirect(1)
window.wm_state('normal')
window.wm_attributes("-alpha", 0.5)
window.mainloop()
