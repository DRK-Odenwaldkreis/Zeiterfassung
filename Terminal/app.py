#!/usr/bin/python3
# coding=utf-8
from tkinter import *
import sqlite3
import time

from booking import *
from readconfig import read_config

class App:
    def __init__(self, master):
        self.dbName = read_config("DB", "dbFile")
        self.master= master
        self.master.configure(background='white')
        self.frame = Frame(self.master)
        self.image = PhotoImage(file="logo_small.png").subsample(3,3)
        self.logoLabel = Label(self.frame, image=self.image, borderwidth=0)
        self.logoLabel.grid(column=1, row=0, padx=0, pady=10)
        self.frame.configure(background='white')
        self.frame.pack(side='top')
        self.inputTextField = Entry(
            self.frame, width=0, font=("Helvetica", 0), bg='white', justify=CENTER, bd=0, fg='white', insertontime=0)
        self.inputTextField.grid(column=1, row=1)
        self.inputTextField.bind(
            '<Return>', lambda event: self.enter_input(self.inputTextField.get()))
        self.scanLabel = Label(
            self.frame, text="Bitte scannen!", font=("Helvetica", 32), bg='white')
        self.scanLabel.grid(column=1, row=2, padx=0, pady=20)
        self.directionLabel = Label(
            self.frame, text="", font=("Helvetica", 86),bg='white')
        self.directionLabel.grid(column=1, row=5, padx=0, pady=10)
        self.inputTextField.focus_set()
    
    def show_goodbye(self):
        self.name = self
        self.subInfoLabel = Label(
            self.frame, text="Danke, xy", font=("Helvetica", 32), bg='white')
        self.subInfoLabel.grid(column=1, row=6, padx=0, pady=10)
        self.subInfoLabel.after(1000, self.subInfoLabel.destroy())

    

    def enter_input(self, hash):
        self.hash = hash
        print(self.hash)
        try:
            self.event = ScanEvent(self.hash)
            self.event.check_validity()
            self.event.get_personal_number()
            self.event.check_dead_time()
            self.event.check_open_entries()
            """if self.event.direction == "Dienstbegin":
                self.event.create_shift()
                self.text = "KOMMEN"
            elif self.event.direction == "Dienstende":
                self.event.close_shift()
                self.text = "GEHEN"
                self.show_goodbye()
            self.directionLabel.configure(
                text=self.text, bg="Green")
            self.directionLabel.after(
            1000, lambda: self.directionLabel.config(bg='white', text=""))"""
        except QRInvalid:
            self.directionLabel.configure(text="Ungültiger QR Code", bg="Red")
            self.directionLabel.after(2000, lambda: self.directionLabel.config(bg='white', text=""))
        except PersonUnknown:
            self.directionLabel.configure(text="QR Code unbekannt", bg="Red")
            self.directionLabel.after(2000, lambda: self.directionLabel.config(bg='white', text=""))
        except DeadTime:
            self.directionLabel.configure(text="Zeiten bereits gebucht", bg="Blue")
            self.directionLabel.after(2000, lambda: self.directionLabel.config(bg='white', text=""))
        except UnknownState:
            self.directionLabel.configure(text="Unbekannter Fehler", bg="Red")
            self.directionLabel.after(2000, lambda: self.directionLabel.config(bg='white', text=""))
        except Exception as e:
            print("Error in ScanEvent")
            print(e)
        finally:
            self.inputTextField.delete(0, END)
