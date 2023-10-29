import PySimpleGUI as sg
import keyboard
import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode, Key

toggleKey = Key.f6

stopThread = False
active = True
mouse = Controller()
activeThread = False

listener = None


def auto_click_interval():
    time_sleep = int(values['Minutes']) * 60 + int(values['Seconds']) + int(values['Milliseconds']) / 1000
    if time_sleep == 0:
        time_sleep = 0.001
    while not stopThread:
        if active:
            mouse.click(Button.left, 1)
        time.sleep(time_sleep)
        print("Clicked at " + str(time_sleep))
    print("Thread clicker finished.")


def stop_check(key):
    if key == toggleKey:
        global active
        active = not active


def listen_for_key():
    global listener
    with Listener(on_press=stop_check) as l:
        listener = l
        listener.join()
    print("Thread listener finished.")


key_listener_thread = threading.Thread(target=listen_for_key)
key_listener_thread.start()

input_text_params = {
    "size": (5, 2),
    "justification": "right",
    "default_text": "0"
}

button_params = {
    "size": (15, 1)
}
# Define the layout for your window
layout = [
    [sg.Text("Click interval: ", font=("Helvetica", 12, "normal"))],
    [sg.Text("Minutes:"), sg.InputText(**input_text_params, key="Minutes"), sg.Text("Seconds:"), sg.InputText(**input_text_params, key="Seconds"), sg.Text("Milliseconds:"), sg.InputText(**input_text_params, key="Milliseconds")],
    [sg.Button("Start(F6)", **button_params), sg.Push(), sg.Button("Stop(F6)", **button_params)],
    [sg.Button("Save", **button_params), sg.Push(), sg.Button("Close", **button_params)]
]

# Create the window
window = sg.Window("Autoclicker", layout)


# Event loop
while True:
    event, values = window.read()

    print(event, values)

    if event == sg.WIN_CLOSED or event == "Close":
        stopThread = True
        activeThread = False
        if listener is not None:
            listener.stop()
        break

    if event == "Start(F6)":
        time.sleep(2)
        print("Autoclicker started 1.")
        stopThread = False

        clickThread = threading.Thread(target=auto_click_interval)
        clickThread.start()
        activeThread = True



        print("Autoclicker started 2.")

    if event == "Stop(F6)":
        stopThread = True
        activeThread = False


window.close()