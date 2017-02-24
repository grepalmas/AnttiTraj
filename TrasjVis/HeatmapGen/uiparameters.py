import Tkinter as tk
import tkFileDialog
import tkColorChooser

from Tkinter import LabelFrame, IntVar, StringVar
from Tkinter import Label
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Spinbox
from Tkinter import Listbox
from Tkinter import Frame

import ttk

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
        
        line.append("-ksize")
        line.append(self.kernelSizeSBox.get())

        line.append("-stat")
        line.append(self.statListBoxVar.get())
        
        line.append("-gamma")
        line.append(self.gammaSbox.get())

        line.append("-dpi")
        line.append(self.dpiSbox.get())

        line.append("-color1")
        color_list = self.color1Entry.get().split(",")
        for color in color_list:
            line.append(color)

        line.append("-color2")
        color_list = self.color2Entry.get().split(",")
        for color in color_list:
            line.append(color)

        line.append("-imgfilter")
        line.append(self.filter_box_value.get())
        
        if self.contoursVar.get() == 1:
            line.append("-showcontours")

        if self.flipXVar.get() == 1:
            line.append("-flipx")

        if self.flipYVar.get() == 1:
            line.append("-flipy")

        line.append("-transform")
        line.append(self.transform_box_value.get())

        if self.saveKDEVar:
            line.append("-saveKDE")

        if aslist: return line

        return " ".join(line)

    def PickColor(self):
        
        color = tkColorChooser.askcolor()
        rgbColor = color[0]
        colorString = str('%.2f'%(rgbColor[0]/255.0)) + "," + str('%.2f'%(rgbColor[1]/255.0)) + "," + str('%.2f'%(rgbColor[2]/255.0))
        self.color1Entry.delete(0, tk.END)
        self.color1Entry.insert(0, colorString + ",0")

        self.color2Entry.delete(0, tk.END)
        self.color2Entry.insert(0, colorString + ",1")

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
        self.folderEntry = Entry(self.lframe)
        self.folderEntry.insert(0,"No Folder")
        self.folderEntry.grid(row = 0, column = 1)
        self.folderButton = Button(self.lframe, text="Set Folder", command = self.SetFolderPath)
        self.folderButton.grid(row = 0, column = 2)

        self.columnsLabel = Label(self.lframe, text="Columns: ")
        self.columnsLabel.grid(row = 1, column = 0)
        self.columnsEntry = Entry(self.lframe)
        self.columnsEntry.insert(0,"Column names space-separated")
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
        self.statListBoxVar = StringVar()
        self.statListBox = ttk.Combobox(self.lframe, textvariable = self.statListBoxVar)
        self.statListBox['values'] = ('mean', 'sum')
        self.statListBox.current(0)
        self.statListBox.grid(row = 4, column = 1)

        #self.filter_box = ttk.Combobox(self.lframe, textvariable = self.filter_box_value)
        #self.filter_box['values'] = ('none', 'nearest', 'bilinear', 'bicubic', 'spline16',\
        #                             'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',\
        #                             'catrom', 'bessel', 'mitchell', 'sinc', 'lanczos','gaussian')
        #self.filter_box.current(11)
        #self.filter_box.grid(row = 11, column = 1)

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

        self.kernelSizeLabel = Label(self.lframe, text="KDE kernel size: ")
        self.kernelSizeLabel.grid(row = 8, column = 0)
        self.kernelSizeSBox = Spinbox(self.lframe, increment = 1)
        self.SetValueToSBox(self.kernelSizeSBox, 0.3)
        self.kernelSizeSBox.grid(row = 8, column = 1)

        self.color1Label = Label(self.lframe, text="Color Map Color1: ")
        self.color1Label.grid(row = 9, column = 0)
        self.color1Entry = Entry(self.lframe)
        self.color1Entry.grid(row = 9, column = 1)
        self.color1Entry.insert(0, "1,0,0,0")

        self.color2Label = Label(self.lframe, text="Color Map Color2: ")
        self.color2Label.grid(row = 10, column = 0)
        self.color2Entry = Entry(self.lframe)
        self.color2Entry.grid(row = 10, column = 1)
        self.color2Entry.insert(0, "1,0,0,1")

        self.colorPickButton = Button(self.lframe, text = "Pick color", command = self.PickColor)
        self.colorPickButton.grid(row = 9, column = 2)


        self.filter_label = Label(self.lframe, text="Image filters")
        self.filter_label.grid(row = 11, column = 0)
        self.filter_box_value = StringVar()
        self.filter_box = ttk.Combobox(self.lframe, textvariable = self.filter_box_value)
        self.filter_box['values'] = ('none', 'nearest', 'bilinear', 'bicubic', 'spline16',\
                                     'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',\
                                     'catrom', 'bessel', 'mitchell', 'sinc', 'lanczos','gaussian')
        self.filter_box.current(11)
        self.filter_box.grid(row = 11, column = 1)
        
        self.contoursLabel = Label(self.lframe, text="Show contours")
        self.contoursLabel.grid(row = 12, column = 0)
        self.contoursVar = IntVar()
        self.contoursCheck = Checkbutton(self.lframe, text ="", onvalue = 1, offvalue = 0, variable = self.contoursVar)
        self.contoursCheck.grid(row = 12, column = 1)

        self.flipXLabel = Label(self.lframe, text="Flip X")
        self.flipXLabel.grid(row = 13, column = 0)
        self.flipXVar = IntVar()
        self.flipXCheck = Checkbutton(self.lframe, text ="", onvalue = 1, offvalue = 0, variable = self.flipXVar)
        self.flipXCheck.grid(row = 13, column = 1)

        self.flipYLabel = Label(self.lframe, text="Flip Y")
        self.flipYLabel.grid(row = 14, column = 0)
        self.flipYVar = IntVar()
        self.flipYCheck = Checkbutton(self.lframe, text ="", onvalue = 1, offvalue = 0, variable = self.flipYVar)
        self.flipYCheck.grid(row = 14, column = 1)
        
        self.transform_label = Label(self.lframe, text="Data transformation")
        self.transform_label.grid(row = 15, column = 0)
        self.transform_box_value = StringVar()
        self.transform_box = ttk.Combobox(self.lframe, textvariable = self.transform_box_value)
        self.transform_box['values'] = ('none', 'log10', 'sqrt', 'reciprocal')
        self.transform_box.current(0)
        self.transform_box.grid(row = 15, column = 1)

        self.saveKDELavel = Label(self.lframe, text="Save Densities")
        self.saveKDELavel.grid(row = 16, column = 0)
        self.saveKDEVar = IntVar()
        self.saveKDECheck = Checkbutton(self.lframe, text ="", onvalue = 1, offvalue = 0, variable = self.saveKDEVar)
        self.saveKDECheck.grid(row = 16, column = 1)

        self.lframe.pack()
        
        self.ButtonFrame = Frame(self.master)
        self.applyButton = tk.Button(self.ButtonFrame, text ="Apply", command = self.Apply)
        self.applyButton.grid(row = 0, column = 0)
        self.closeButton = tk.Button(self.ButtonFrame, text ="Close", command = self._quit)
        self.closeButton.grid(row = 0, column = 1)
        self.saveButton = tk.Button(self.ButtonFrame, text ="Save Command Line", command = self.SaveParams)
        self.saveButton.grid(row = 0, column = 2)

        self.ButtonFrame.pack()