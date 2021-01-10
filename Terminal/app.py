#!/usr/bin/python3
# coding=utf-8
from tkinter import *
import time
from failoverdatabase import create_backup_event
from booking import *
from readconfig import read_config
import logging
import threading

logger = logging.getLogger('Application')
logger.debug('Logger for UI Application was initialised')

afterIDMainLabel = None

class App:
    def __init__(self, master):
        logger.debug('Constructor was called')
        self.master= master
        self.master.configure(background='white')
        logger.debug('Setting frame')
        self.frame = Frame(self.master)
        self.image = PhotoImage(file="./logo.png").zoom(2,2)
        logger.debug('Setting Logo')
        self.logoLabel = Label(self.frame, image=self.image, borderwidth=0)
        self.logoLabel.grid(column=1, row=0, padx=0, pady=10)
        self.frame.configure(background='white')
        self.frame.pack(side='top')
        logger.debug('Setting Textfield for input')
        self.inputTextField = Entry(
            self.frame, width=0, font=("Helvetica", 0), bg='white', justify=CENTER, bd=0, fg='white', insertontime=0)
        self.inputTextField.grid(column=1, row=1)
        self.inputTextField.bind(
            '<Return>', lambda event: self.enter_input(self.inputTextField.get()))
        logger.debug('Setting labels for Messages')
        self.scanLabel = Label(
            self.frame, text="Bitte scannen!", font=("Helvetica", 48), bg='white')
        self.scanLabel.grid(column=1, row=2, padx=0, pady=20)
        self.mainLabel = Label(
            self.frame, text="", font=("Helvetica", 86),bg='white')
        self.mainLabel.grid(column=1, row=5, padx=0, pady=70)
        self.subInfoLabel = Label(
            self.frame, text="", font=("Helvetica", 40), bg='white')
        self.subInfoLabel.grid(column=1, row=6, padx=0, pady=50)
        logger.debug('Setting the focus to text field')
        self.inputTextField.focus_set()

    
    def enter_input(self, hash):
        global afterIDMainLabel
        self.hash = hash
        logger.debug('The following input was received, starting event process: %s' % (self.hash))
        try:
            if afterIDMainLabel is not None:
                self.mainLabel.after_cancel(afterIDMainLabel)
                self.subInfoLabel.config(bg='white', text="")
                afterIDMainLabel = None
            self.event = ScanEvent(self.hash)
            self.event.check_validity()
            #After check validity he backup inside local database can already be writen due to the fact that only hash is required.
            threadFailoverDatabase = threading.Thread(target=create_backup_event, kwargs=dict(hash=self.hash), daemon=True)
            threadFailoverDatabase.start()
            self.event.get_personal_number()
            self.event.check_dead_time()
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
                logging.error("This is an abnormal state within enter input") 
                raise UnknownState
            self.mainLabel.configure(text=self.textMain, bg="Green")
            self.subInfoLabel.configure(text=self.textSub)
            afterIDMainLabel = self.mainLabel.after(
                1500, lambda: self.mainLabel.config(bg='white', text=""))
        except DatabaseDisconnect:
            logger.warning('Displaying that no connectivity but values will be stored')
            self.mainLabel.configure(
                text="Server offline, Scan gespeichert", bg="Red")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except QRInvalid:
            logger.debug('Displaying that QR is not valid')
            self.mainLabel.configure(text="Ungültiger QR Code", bg="Red")
            afterIDMainLabel = self.mainLabel.after(2000, lambda: self.mainLabel.config(bg='white', text=""))
        except PersonUnknown:
            logger.debug('Displaying Person is unknown')
            self.mainLabel.configure(text="Mitarbeiter unbekannt", bg="Red")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except DeadTime:
            logger.debug('Displaying that code was already scanned')
            self.mainLabel.configure(text="Zeit bereits gebucht", bg="Blue")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except UnknownState:
            logger.debug('Displaying that state is unknown')
            self.mainLabel.configure(text="Unbekannter Fehler", bg="Red")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except UnableToWrite:
            logger.debug('Displaying that time could not be stored')
            self.mainLabel.configure(text="Zeiten konnten nicht gebucht werden", bg="Red")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except UnknownError:
            logger.debug('Displaying that unknown error occured')
            self.mainLabel.configure(text="Unbekannter Fehler", bg="Red")
            afterIDMainLabel = self.mainLabel.after(
                2000, lambda: self.mainLabel.config(bg='white', text=""))
        except Exception as e:
            logger.error('The following error occured in enter input: %s' % (e))
        finally:
            self.subInfoLabel.after(1500, lambda: self.subInfoLabel.config(bg='white', text=""))
            logger.debug('Wiping all information from screen')
            self.inputTextField.delete(0, END)
