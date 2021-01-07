#!/usr/bin/python3
# coding=utf-8
from tkinter import *
import time
from failoverdatabase import create_backup_event
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
            self.frame, text="Bitte scannen!", font=("Helvetica", 48), bg='white')
        self.scanLabel.grid(column=1, row=2, padx=0, pady=20)
        self.mainLabel = Label(
            self.frame, text="", font=("Helvetica", 86),bg='white')
        self.mainLabel.grid(column=1, row=5, padx=0, pady=70)
        self.subInfoLabel = Label(
            self.frame, text="", font=("Helvetica", 40), bg='white')
        self.subInfoLabel.grid(column=1, row=6, padx=0, pady=50)
        self.inputTextField.focus_set()


    
    def enter_input(self, hash):
        self.hash = hash
        try:
            self.event = ScanEvent(self.hash)
            self.event.check_validity()
            self.event.get_personal_number()
            self.event.check_dead_time()
            create_backup_event(self.hash)
            self.event.check_open_entries()
            if self.event.direction == "Dienstbegin":
                self.event.create_shift()
                self.textMain = "KOMMEN"
                self.textSub = "Hallo %s %s" %(self.event.vorname, self.event.nachname)
            elif self.event.direction == "Dienstende":
                self.event.close_shift()
                self.textMain = "GEHEN"
                self.textSub = "Danke %s %s - Dienstdauer: %s:%s" % (
                    self.event.vorname, self.event.nachname, self.event.shiftDurationHours, self.event.shiftDurationMinutes)
            else:
                raise UnknownState
            self.mainLabel.configure(text=self.textMain, bg="Green")
            self.subInfoLabel.configure(text=self.textSub)
            self.mainLabel.after(1500, lambda: self.mainLabel.config(bg='white', text=""))
            self.subInfoLabel.after(1500, lambda: self.subInfoLabel.config(bg='white', text=""))
        except QRInvalid:
            self.mainLabel.configure(text="Ungültiger QR Code", bg="Red")
            self.mainLabel.after(2000, lambda: self.mainLabel.config(bg='white', text=""))
        except PersonUnknown:
            self.mainLabel.configure(text="Mitarbeiter unbekannt", bg="Red")
            self.mainLabel.after(2000, lambda: self.mainLabel.config(bg='white', text=""))
        except DeadTime:
            self.mainLabel.configure(text="Zeit bereits gebucht", bg="Blue")
            self.mainLabel.after(2000, lambda: self.mainLabel.config(bg='white', text=""))
        except UnknownState:
            self.mainLabel.configure(text="Unbekannter Fehler", bg="Red")
            self.mainLabel.after(2000, lambda: self.mainLabel.config(bg='white', text=""))
        except UnableToWrite:
            self.mainLabel.configure(text="Zeiten konnten nicht gebucht werden", bg="Red")
            self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        finally:
            self.inputTextField.delete(0, END)
