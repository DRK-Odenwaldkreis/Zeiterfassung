#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Zeiterfassung.

# DRK Zeiterfassung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# DRK Zeiterfassung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DRK Zeiterfassung.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *
import time
from utils.readconfig import read_config
from utils.failoverdatabase import create_backup_event
import logging
import threading
import requests
import json
from PIL import Image, ImageTk
from io import BytesIO
from utils.token import refresh_token, get_token

logger = logging.getLogger(__name__)
logger.debug('Logger for UI Application was initialised')

afterIDMainLabel = None
subInfoIDLabel = None
waitingTime = read_config('Terminal','waitingTime')
class App:
    def __init__(self, master):
        logger.debug('Constructor was called')
        self.master= master
        self.master.configure(background='white')
        logger.debug('Setting frame')
        self.frame = Frame(self.master)
        logoURL = read_config('Terminal','logo')
        u = requests.get(logoURL)
        self.image = ImageTk.PhotoImage(Image.open(BytesIO(u.content)))
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
            self.frame, text="Bitte scannen!", font=("Helvetica", 48), bg='white', fg='black')
        self.scanLabel.grid(column=1, row=2, padx=0, pady=20)
        self.mainLabel = Label(
            self.frame, text="", font=("Helvetica", 86),bg='white')
        self.mainLabel.grid(column=1, row=5, padx=0, pady=70)
        self.subInfoLabel = Label(
            self.frame, text="", font=("Helvetica", 40), bg='white')
        self.subInfoLabel.grid(column=1, row=6, padx=0, pady=50)
        logger.debug('Setting the focus to text field')
        self.inputTextField.focus_set()

    
    def enter_input(self,hash):
        global afterIDMainLabel
        global subInfoIDLabel
        self.hash = hash
        logger.debug('The following input was received, starting event process: %s' % (self.hash))
        try:
            if afterIDMainLabel is not None:
                    self.mainLabel.after_cancel(afterIDMainLabel)
                    if subInfoIDLabel is not None:
                        self.subInfoLabel.after_cancel(subInfoIDLabel)
                    self.subInfoLabel.config(bg='white', text="")
                    afterIDMainLabel = None
                    subInfoIDLabel = None
            headers = {}
            headers['Content-Type'] = 'application/json'
            headers['Authorization'] = f'Bearer {get_token()}'
            payload = {}
            url = read_config('Server','endpoint')
            response = requests.request("POST", url + self.hash, headers=headers, data=payload)
            if response.status_code != 200:
                create_backup_event(self.hash)
                self.textMain = "Server offline, Scan gespeichert"
                self.textSub = ''
                self.mainLabelColor = 'Red'
                self.textColor = 'black'
                self.type = 'Error'
                refresh_token()
            else:
                self.content = response.json()
                self.textMain = self.content['textMain']
                self.textSub = self.content['textSub']
                self.mainLabelColor = self.content['mainLabel']
                self.textColor = self.content['textColor']
                self.type = self.content['type']
            self.mainLabel.configure(text=self.textMain, bg=self.mainLabelColor, fg=self.textColor)
            if len(self.textSub) > 0:
                self.subInfoLabel.configure(text=self.textSub, bg=self.mainLabelColor, fg=self.textColor)
        except Exception as e:
            logger.error('The following error occured: %s' % (e))
            self.mainLabel.configure(text="Bitte IT informieren", bg="Red",fg=self.textColor)
        finally:
            subInfoIDLabel= self.subInfoLabel.after(
                waitingTime, lambda: self.subInfoLabel.config(bg='white', text="", fg=self.textColor))
            afterIDMainLabel = self.mainLabel.after(
                waitingTime, lambda: self.mainLabel.config(bg='white', text="", fg=self.textColor))
            logger.debug('Wiping all information from screen')
            self.inputTextField.delete(0, END)