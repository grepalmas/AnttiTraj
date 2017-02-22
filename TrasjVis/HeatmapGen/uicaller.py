import Tkinter as tk

from uiparameters import UiParameters

master_app = tk.Tk()

main_window = UiParameters(master_app)

master_app.mainloop()

def _quit(self):    
        master_app.destroy() 
        master_app.quit()

