import Tkinter as tk

from Tkinter import LabelFrame
from Tkinter import Label
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Spinbox
from Tkinter import Listbox

class UiParameters:
    
    def SetFolderPath():
        return
        
    def Apply():
        return
    
    def Close():
        return

    def SaveParams():
        return

    def SetValueToSBox(self, sbox, value):

        sbox.delete(0,"end")
        sbox.insert(0, str(value))

    def __init__(self, master):
        
        self.master = master
        self.lframe = LabelFrame(self.master, text = "Parameters")
        
        self.folderLabel = Label(self.lframe, text="Folder Path: ", command = self.SetFolderPath)
        self.folderLabel.grid(row = 0, column = 0)        
        self.folderEntry = Entry(self.lframe, text="No Folder")
        self.folderEntry.grid(row = 0, column = 1)
        self.folderButton = Button(self.lframe, text="Open")
        self.folderEntry.grid(row = 0, column = 2)

        self.columnsLabel = Label(self.lframe, text="Columns: ")
        self.columnsLabel.grid(row = 1, column = 0)
        self.columnsEntry = Entry(self.lframe, text="Column names space-separated")
        self.columnsEntry.grid(row = 1, column = 1)
        
        self.shotLabel = Label(self.lframe, text="Screenshot")
        self.shotLabel.grid(row = 2, column = 0)
        self.shotCheck = Checkbutton(self.lframe, text ="")
        self.shotCheck.grid(row = 2, column = 1)

        self.dpiLabel = Label(self.lframe, text="DPI: ")
        self.dpiLabel.grid(row = 3, column = 0)
        self.dpiSbox = Spinbox(self.lframe)
        self.dpiSbox.grid(row = 3, column = 1)
        self.SetValueToSBox(self.dpiSbox, 120)

        self.statLabel = Label(self.lframe, text="Stat: ")
        self.statLabel.grid(row = 4, column = 0)
        self.statListBox = Listbox(self.lframe)
        self.statListBox.pack()
        self.statListBox.insert(END, "Average")
        self.statListBox.insert(END, "Sum")
        self.statListBox.grid(row = 4, column = 1)

        self.gammaLabel = Label(self.lframe, text="Gamma factor: ")
        self.gammaLabel.grid(row = 5, column = 0)
        self.gammaSbox = Spinbox(self.lframe, format="%.2f")
        self.gammaSbox.grid(row = 5, column = 1)
        self.SetValueToSBox(self.gammaSbox, 1.0)

        self.resXLabel = Label(self.lframe, text="Res X: ")
        self.resXLabel.grid(row = 5, column = 0)
        self.resXbox = Spinbox(self.lframe)
        self.SetValueToSBox(self.resXbox, 16)
    
        self.resYLabel = Label(self.lframe, text="Res Y: ")
        self.resYLabel.grid(row = 6, column = 0)
        self.resYbox = Spinbox(self.lframe)
        self.SetValueToSBox(self.resYbox, 8)

        self.ButtonFrame = Frame(self.master)
        self.applyButton = tk.Button(self.ButtonFrame, text ="Apply", command = self.Apply)
        self.applyButton.grid(row = 0, column = 0)
        self.closeButton = tk.Button(self.ButtonFrame, text ="Close", command = self.Close)
        self.closeButton.grid(row = 0, column = 1)
        self.saveButton = tk.Button(self.ButtonFrame, text ="Save Command Line", command = self.SaveParams)
        self.saveButton.grid(row = 0, column = 2)
        