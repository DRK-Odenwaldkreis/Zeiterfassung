#!/usr/bin/python3
# coding=utf-8
import sys
from tkinter import *
from app import App

window = Tk()
window.title("Zeitenbuchungssystem DRK Odenwaldkreis")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(str(width) + "x" + str(height))
#window.config(cursor="none")
app = App(window)
try:
    window.mainloop()
except KeyboardInterrupt():
    sys.exit(0)
except:
    pass
