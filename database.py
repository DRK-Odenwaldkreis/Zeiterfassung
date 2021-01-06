#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Database v 0.1

#Copyright Philipp Scior philipp.scior@drk-forum.de


import sqlite3
import datetime
import hashlib

# from pdf import PDFgenerator


class Database_error(Exception):
    pass


class Database:

    print_list = []

# Constructor
    def __init__(self,new):

        self.connection = sqlite3.connect("./dummy.db")
        self.connection.text_factory=str


        self.cursor = self.connection.cursor()

        if new == 1:
            try:
                self.cursor.execute("DROP TABLE zeiten")
                self.cursor.execute("DROP TABLE personal")
            except Exception as e:
                pass
            
        

            self.sql_make_personal= """
            CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY, 
            nachname VARCHAR(50),
            vorname VARCHAR(50),
            personalnummer INT UNIQUE,
            hash CHAR(64) UNIQUE
            );
            """

            self.sql_make_zeiten= """
            CREATE TABLE IF NOT EXISTS zeiten (
            id INTEGER PRIMARY KEY,
            personalnummer INT,
            kommen TIMESTAMP,
            gehen TIMESTAMP,
            art INT
            );
            """
            self.cursor.execute(self.sql_make_personal)
            self.cursor.execute(self.sql_make_zeiten)

#erwartet ein Tupel als input = (Name, Vorname, Personalnummer)
    def neuer_mitarbeiter(self, input):
        hash = hashlib.sha256(input[2]).hexdigest()
        tupel = (input[0], input[1], input[2], hash)
        try:
            self.cursor.execute("INSERT INTO personal VALUES (NULL,?,?,?,?)", tupel)
        except sqlite3.IntegrityError as e:
            raise Database_error("FEHLER: Personalnummer bereits vergeben")
        self.connection.commit()


    def print_mitarbeiter(self):
        self.cursor.execute("SELECT * FROM personal")
        print("Personal:")
        self.result=self.cursor.fetchall()
        for r in self.result:
            print(r)

#Erwartet den hash der personalnummer als input
    def kommen(self, input):
        zeit = datetime.datetime.now()
        hash = (input,)
        self.cursor.execute("SELECT * FROM personal WHERE hash=?", hash)
        result=self.cursor.fetchone()
        tupel = (result[3], zeit)
        self.cursor.execute("INSERT INTO zeiten VALUES (NULL, ?, ?, NULL, 1)", tupel)
        self.connection.commit()

#Erwartet den hash der personalnummer als input
    def gehen(self, input):
        zeit = datetime.datetime.now()
        hash = (input,)
        self.cursor.execute("SELECT * FROM personal WHERE hash=?", hash)
        result=self.cursor.fetchone()
        tupel = (result[3],)
        self.cursor.execute("SELECT * FROM zeiten WHERE personalnummer=? AND gehen IS NULL", tupel)
        self.result=self.cursor.fetchall()
        try:
            tupel2=(zeit,self.result[-1][0])
            self.cursor.execute("UPDATE zeiten SET gehen=? WHERE id=?", tupel2)
        except:
            pass
        if not len(self.result)==1:
            print("Arbeitszeiten nicht vollständig erfasst, bitte Schichtleiter*in aufsuchen")
        # for r in self.result:
            # print(r)

    def history(self):
        self.cursor.execute("SELECT * FROM zeiten")
        self.result=self.cursor.fetchall()
        print("Zeiten:")
        for r in self.result:
            print(r)
        

def main():
    Personal = Database(1)
    try:
        Personal.neuer_mitarbeiter(("Scior", "Philipp", "6000"))
        Personal.neuer_mitarbeiter(("Bayram", "Murat", "6001"))
    except Database_error as e:
        print("Personalnummer schon vergeben")

    Personal.print_mitarbeiter()
    # Personal.kommen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    # Personal.kommen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.gehen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.history()

if __name__ == "__main__":
    main()