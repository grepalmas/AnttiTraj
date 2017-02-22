import Tkinter as tk
import tkFileDialog

from Tkinter import LabelFrame, IntVar
from Tkinter import Label
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Spinbox
from Tkinter import Listbox
from Tkinter import Frame

import heatmap_gen

class UiParameters:
    
    def _quit(self):
    
        self.master.destroy() 
        self.master.quit()

    def MakeCommandLine(self, aslist):

        #"-open C:\Projects\AnttiTraj\data\test -vis x y trialtime -screenshot -res 80 40 -stat mean -gamma 2.0 -dpi 240"
        
        line = ["python heatmap_gen.py"] 
        line.append("-open")
        line.append(self.folderEntry.get())
        
        line.append("-vis")
        columns = self.columnsEntry.get().split(" ")
        for column in columns:
            line.append(column)
        
        if self.varShot.get() == 1:
            line.append("-screenshot")
        
        line.append("-res")
        line.append(self.resXbox.get())
        line.append(self.resYbox.get())
        
        line.append("-stat")
        line.append(self.statListBox.get(self.statListBox.curselection()))
        
        line.append("-gamma")
        line.append(self.gammaSbox.get())

        line.append("-dpi")
        line.append(self.dpiSbox.get())
        
        if aslist: return line

        return " ".join(line)

    def SetFolderPath(self):

        options = {}
        options['parent'] = self.master
        options['title'] = 'Set data folder path'
        options['initialdir'] = './'

        dir = tkFileDialog.askdirectory(**options)
        if dir == None:
            return
        else:
           self.folderEntry.delete(0, tk.END)
           self.folderEntry.insert(0, dir)

        return
        
    def Apply(self):
    
        commandLine = self.MakeCommandLine(True)
        heatmap_gen.main(commandLine)

        return

    def SaveParams(self):

        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('txt', '.txt')]
        options['initialdir'] = './'
        options['parent'] = self.master
        options['title'] = 'Save Command Line'

        save_file = tkFileDialog.asksaveasfile(mode = 'w', **options)

        if save_file == None:
            return
        
        commandLine = self.MakeCommandLine(False)

        outFile = open(save_file.name, "w")
        outFile.write(commandLine)
        outFile.close()

        return

    def SetValueToSBox(self, sbox, value):

        sbox.delete(0,  tk.END)
        sbox.insert(0, str(value))

    def __init__(self, master):
        
        self.master = master
        self.lframe = LabelFrame(self.master, text = "Parameters")
        
        self.folderLabel = Label(self.lframe, text="Folder Path: ")
        self.folderLabel.grid(row = 0, column = 0)        
        self.folderEntry = Entry(self.lframe, text="No Folder")
        self.folderEntry.grid(row = 0, column = 1)
        self.folderButton = Button(self.lframe, text="Set Folder", command = self.SetFolderPath)
        self.folderButton.grid(row = 0, column = 2)

        self.columnsLabel = Label(self.lframe, text="Columns: ")
        self.columnsLabel.grid(row = 1, column = 0)
        self.columnsEntry = Entry(self.lframe, text="Column names space-separated")
        self.columnsEntry.grid(row = 1, column = 1)
        
        self.varShot = IntVar()
        self.shotLabel = Label(self.lframe, text="Screenshot")
        self.shotLabel.grid(row = 2, column = 0)
        self.shotCheck = Checkbutton(self.lframe, text ="", onvalue = 1, offvalue = 0, variable = self.varShot)
        self.shotCheck.grid(row = 2, column = 1)

        self.dpiLabel = Label(self.lframe, text="DPI: ")
        self.dpiLabel.grid(row = 3, column = 0)
        self.dpiSbox = Spinbox(self.lframe, increment = 1)
        self.dpiSbox.grid(row = 3, column = 1)
        self.SetValueToSBox(self.dpiSbox, 120)

        self.statLabel = Label(self.lframe, text="Stat: ")
        self.statLabel.grid(row = 4, column = 0)
        self.statListBox = Listbox(self.lframe, height = 2)
        self.statListBox.insert(tk.END, "mean")
        self.statListBox.insert(tk.END, "sum")
        self.statListBox.pack()
        self.statListBox.grid(row = 4, column = 1)

        self.gammaLabel = Label(self.lframe, text="Gamma factor: ")
        self.gammaLabel.grid(row = 5, column = 0)
        self.gammaSbox = Spinbox(self.lframe, format="%.2f", increment = 0.1)
        self.gammaSbox.grid(row = 5, column = 1)
        self.SetValueToSBox(self.gammaSbox, 1.0)

        self.resXLabel = Label(self.lframe, text="Res X: ")
        self.resXLabel.grid(row = 6, column = 0)
        self.resXbox = Spinbox(self.lframe, increment = 1)
        self.SetValueToSBox(self.resXbox, 16)
        self.resXbox.grid(row = 6, column = 1)
    
        self.resYLabel = Label(self.lframe, text="Res Y: ")
        self.resYLabel.grid(row = 7, column = 0)
        self.resYbox = Spinbox(self.lframe, increment = 1)
        self.SetValueToSBox(self.resYbox, 8)
        self.resYbox.grid(row = 7, column = 1)

        self.lframe.pack()

        self.ButtonFrame = Frame(self.master)
        self.applyButton = tk.Button(self.ButtonFrame, text ="Apply", command = self.Apply)
        self.applyButton.grid(row = 0, column = 0)
        self.closeButton = tk.Button(self.ButtonFrame, text ="Close", command = self._quit)
        self.closeButton.grid(row = 0, column = 1)
        self.saveButton = tk.Button(self.ButtonFrame, text ="Save Command Line", command = self.SaveParams)
        self.saveButton.grid(row = 0, column = 2)

        self.ButtonFrame.pack()