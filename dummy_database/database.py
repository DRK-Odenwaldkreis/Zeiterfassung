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

        self.connection = sqlite3.connect("/Users/philippscior/Zeiterfassung/dummy_database/dummy.db")
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
        # hash = hashlib.sha256(input[2]).hexdigest()
        hash = hashlib.sha256(str(input[2]).encode('utf-8')).hexdigest()
        tupel = (input[0], input[1], input[2], hash)
        try:
            self.cursor.execute("INSERT INTO personal VALUES (NULL,?,?,?,?)", tupel)
        except sqlite3.IntegrityError as e:
            raise Database_error("FEHLER: Personalnummer bereits vergeben")
        self.connection.commit()

    def find_mitarbeiter(self, personalnummer):
        self.cursor.execute("SELECT * FROM personal WHERE personalnummer=?", (personalnummer,))
        self.result=self.cursor.fetchone()
        return self.result[1], self.result[2]

    def print_mitarbeiter(self):
        self.cursor.execute("SELECT * FROM personal")
        print("Personal:")
        self.result=self.cursor.fetchall()
        for r in self.result:
            print(r)

#Erwartet den hash der personalnummer als input
    def kommen(self, input):
        zeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hash = (input,)
        self.cursor.execute("SELECT * FROM personal WHERE hash=?", hash)
        result=self.cursor.fetchone()
        tupel = (result[3], zeit)
        self.cursor.execute("INSERT INTO zeiten VALUES (NULL, ?, ?, NULL, 1)", tupel)
        self.connection.commit()

#Erwartet den hash der personalnummer als input
    def gehen(self, input):
        zeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    def monatsuebersicht_einzeln(self, personalnummer, monat):
        if monat < 9:
            dummy1 = "0{}".format(monat)
            dummy2 = "0{}".format(monat+1)
        elif monat==9:
            dummy1 = "0{}".format(monat)
            dummy2 = "{}".format(monat+1)
        else:
            dummy1 = "{}".format(monat)
            dummy2 = "{}".format(monat+1)
        tupel = (personalnummer, "2021-{}-01 00:00:00.000000".format(dummy1),"2021-{}-01 00:00:00.000000".format(dummy2))
        self.cursor.execute("SELECT * FROM zeiten WHERE personalnummer=? AND kommen > ? AND kommen < ? AND gehen IS NOT NULL", tupel)
        self.result = self.cursor.fetchall()  
        # print(self.result)
        return self.result

    def dienst_anlegen(self, personalnummer, anfang, ende, art):
        tupel = (personalnummer, datetime.datetime.strptime(anfang, '%Y-%m-%d %H:%M:%S.%f'), datetime.datetime.strptime(ende, '%Y-%m-%d %H:%M:%S.%f'), art)
        self.cursor.execute("INSERT INTO zeiten VALUES (NULL, ?, ?, ?, ?)", tupel)
        self.connection.commit()


def main():
    Personal = Database(0)
    try:
        Personal.neuer_mitarbeiter(("Scior", "Philipp", 6000))
        Personal.neuer_mitarbeiter(("Bayram", "Murat", 6001))
        Personal.neuer_mitarbeiter(("Ducheme", "Marc", 6002))
    except Database_error as e:
        print("Personalnummer schon vergeben")

    Personal.print_mitarbeiter()

    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 2)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 2)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 1)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 3)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 3)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 3)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 3)
    Personal.dienst_anlegen(6001,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 3)
    Personal.dienst_anlegen(6001,"2021-01-06 09:10:00.000000", "2021-01-06 16:50:00.000000", 3)

    Personal.dienst_anlegen(6000,"2021-01-05 09:10:00.000000", "2021-01-05 16:50:00.000000", 2)

    Personal.kommen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.gehen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.kommen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.gehen("f4e99211184a248ac2b1bb736b2f241982bdbfb599a6a1b62d5c50a1cb7ddbe6")
    Personal.kommen("8d284220975da66c6cba4a32aaedfa0b897187d86ed9f7a2419c9bd10a103505")
    Personal.gehen("8d284220975da66c6cba4a32aaedfa0b897187d86ed9f7a2419c9bd10a103505")

    Personal.kommen("00431bea7c112c6c03ed10860af49e6e791fd93819e027c15313a8e313bdaff9")
    

    Personal.history()

    # Personal.monatsuebersicht_einzeln(6001,1)

if __name__ == "__main__":
    main()