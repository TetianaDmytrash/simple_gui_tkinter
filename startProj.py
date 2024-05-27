"""
main file with calling all function
"""
import tkinter

from SpeakChannel import SpeakCOMPort
from UIView import COMPortApp

if __name__ == "__main__":
    app = COMPortApp()
    curFrame = app.create_widgets()
    curPort = app.port_frame(curFrame)

    connectPort = SpeakCOMPort(curPort)
    connectPort.open_channel()

    app.step_period_frame(curFrame)
    app.speak_frame(curFrame)
    app.press_button_frame(curFrame)

    app.mainloop()
