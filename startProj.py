"""
main file with calling all function
"""
import tkinter

from SpeakChannel import SpeakCOMPort
from UIView import COMPortApp

if __name__ == "__main__":
    app = COMPortApp()
    curFrame = app.create_widgets()
    port_combobox = app.port_frame(curFrame)
    step_period_combobox = app.step_period_frame(curFrame)
    response_frame = app.speak_frame(curFrame)

    port_controller = SpeakCOMPort(port_combobox, step_period_combobox, response_frame)
    app.press_button_frame(curFrame, port_controller)

    app.mainloop()
