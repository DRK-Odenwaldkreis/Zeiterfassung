# Zeiterfassung
Eine Lösung zur Zeiterfassung der Helfer im Impfzentrum des Odenwaldkreises.


# Komponenten

Das Projekt besteht aus mehreren Teilanwendungen. Vor Ort gibt es ein Terminal an dem sich jeder Mitarbeiter an- und abmeldet.
Für die Administration haben Schichtleiter, Buchhaltung und Planungsstaab die Möglichkeit auf einer Webanwendung z.B. Mitarbeiter anzulegen oder Tagesreports zu erzeugen.

## Terminalanwendung

Die Terminalanwendung läuft vor Ort auf einem PC, Laptop. Mittels angeschlossenem QR Code Scanner werden die Ausweise der Mitarbeiter beim Betreten und beim Verlassen des Geländes zu Dienstbeginn und Dienstende gescannt. Das erzeugen der QR Codes der Ausweise findet in der Webanwendung statt.

![Ausweis](Pics/ausweis_example.png)


### Getting Started:

Die Terminalanwendung besteht aus mehren Einzelmodulen und kann auch mittels pyinstaller als .exe verpackt werden. 
Hierfür im Ordner Terminal einfach folgenden Befehl nutzen:

```shell
pyinstaller --onefile --windowed main.py
```

Pyinstaller muss dafür installiert sein. 
Wichtig:
Das logo und der Ordner Log müssen händisch mitgenommen werden, d.h. die .exe startet nur, wenn das logo im gleichen Verzeichnis liegt wie die executable und ein Ordner Log existiert.

Die Anwendung kann auch aus der Konsole direkt gestartet werden ohne sie zuvor als executable zu packen. Dafür die requirements installieren via:

```python
pip install -r requirements.txt
```

Gestaterted wird die Anwendung über die main.py.
Loglevel kann dort angepasst werden. Die Logs landen im Ordner Log.

### Ablauf

Der Mitarbeiter scannt seinen Ausweis. Der QR Code wird gelesen es wird geprüft ob es bereits für diesen Tag offene Dienste (Dienstende is NULL) gibt. Wenn nicht, interpretiert das System den Scanvorgang als "KOMMEN".
In der Datenbank wird nun mit der Personalnummer ein Dienstangelegt, die Zeit des Dienstbeginns wird Serverseitig geschrieben. Dienstende bleibt bei diesem Eintrag Null und dienst als Unterscheidungsmerkmal für das Programm der "Richtung". Das der Mitarbeiter seinen Dienst antritt wird ihm mitgeteilt.

<img src=https://recordit.co/4SfpiMsSY5.gif alt="Kommen" width="480">

Gibt es bereits Dienste (Dienstende is NULL), interpretiert das System den Scanvorgang als "GEHEN". Der vorhandene Dienst wird geschlossen, die Zeit Dienstende wird gesetzt.
Dem Mitarbeiter wird die Dienstdauer mitgeteilt. Pausen werden hier nicht abgezogen, es handelt sich also um die reine Bruttozeit.

<img src=https://recordit.co/Ot6s0QmM3r.gif alt="Gehen" width="480">

Da der Scanvorgang sehr schnell sein kann, können Doppelbuchungen entstehen. Daher wird jede Buchung überprüft ob es in den letzten 5s bereits eine Buchung gab. D.h. es existiert eine Totzeit von 5s auf der spalte updated. Dies wird dem Mitarbeiter auch angezeigt und die Buchung nicht weiter verarbeitet.

<img src=https://recordit.co/Ot6s0QmM3r.gif alt="Gehen" width="480">

Sofern ein QR Code von jmd. gescannt wird der nicht im System angelegt ist, wird die Buchung ebenfalls verworfen. Das der Mitarbeiter unbekannt ist wird ebenfalls angezeigt.
Da die QR Codes beim Anegen in der Webanwendung zufällig erzeugt werden, können QR Codes nur schwer "gefälscht" werden.

<img src=https://recordit.co/37FpElcb0I.gif alt="Unbekannt" width="480">

Jeder QR Scan wird ebenfalls auf die korrekte Länge überprüft. Falls irgendein Code an den Scanner gehalten wird, wird die Buchung ebenfalls verworfen.

<img src=https://recordit.co/pF1vAvzVFw.gif alt="Falscher Code" width="480">

Da die Datenbank in einem Rechenzentrum laufen kann, wird jede Scanvorgang in eine lokale SQLite Datenbank geschrieben. Dies dient dazu bei Verbindungsproblemen keine Einträge zu verlieren. Im Falle eines Disconnects wird angezeigt, dass der Server zwar gerade nicht erreichbar ist, aber der Buchungsvorgang registriert wurde.
Innerhalb der SQLite werden nur die gescannten Codes und der Zeitpunkt gespeichert. Es gibt hier kein Mapping auf die Personalnummer. Des Weiteren gibt es keinen direkten Eintrag ob es sich um "Kommen" oder "Gehen" handelt.

<img src=https://recordit.co/tXYJC0PjDR.gif alt="Server Disconnect" width="480">

## Webpage

### Personaldaten

### Zeitkorrektur

### Tagesreports
Der Tagesreport dient dazu, die Dienste des Vortages aufzulisten. Dies kann z.b. per Cron dem Schichtleiter zugesendet werden. Das Layout als Beispiel sieht wie folgt aus:

<img src=Pics/tagesreport_example.png alt="Tagesreport Beispiel" width="480">

Nachts werden via Konfiguration in phpmyadmin alle offenen Dienste automatisch geschlossen. Dies wird in der Spalte "AutoClose" auch markiert, so dass im Report die Zeiteinträge die vermutlich fehlerhaft sind farblich markiert werden.

Der nächtliche Autoclose wird konfiguriert mit:

```mysql
CREATE EVENT `Nightly AutoClose` ON SCHEDULE EVERY 23 DAY STARTS '2021-01-01 14:49:49' ENDS '2021-12-31 14:49:49' ON COMPLETION NOT PRESERVE ENABLE DO Update Dienste SET Dienstende = current_timestamp(), AutoClosed = '1' WHERE Dienstende is NULL
```

Das setzten der pdf kann unter TagesreportPDF/pdfcreator/pdf.py angepasst werden. Ausführen der job.pdf ohne Argumente erzeugt einen Tagesreport des vergangenen Tages. 

```python 
python job.py
```

Beim Übergaben eines Datums mittels 'YYYY-MM-DD wird der Tagesreport für den übergebenen Tag erzeugt.

```python 
python job.py '2021-01-11'
```

Die Reports liegen im Ordner Reports im Überverzeichnis. D.h. der Ordner muss ggf. erste händisch angelegt werden. Gleiches gilt für den Ordner Logs.

Aus der Webapplikation kann dieser Report ebenfalls erzeugt werden. Hierfür den Tag wählen und auf PDF-Report klicken. Der Report wird zum Download angeboten.

<img src=Pics/tagesreport_web_example.png alt="Tagesreport Webansicht" width="480">

### Einzelabrechnungen
Einzelabrechnugnen werden verwendet um pro Mitarbeiter eine Ansicht der geleisteten Dienste zu erzeugen.

Das setzten der pdf kann unter EinzelabrechnungpDF/pdfcreator/pdf.py angepasst werden. Ausführen der job.pdf kann in zwei Varianten erfolgen: 

```python 
python job.py MONAT JAHR ANFORDERER PERSONALNUMMER
```
Hierbei steht Monat und Jahr für den Monat/Jahr der Einzelnachweisanforderung. Der Anforderer als ID ist die ID des in der Webapplikation angelegten Users. Diese wird beim übergeben eines 4 Arguments, der Personalnummer, nicht verwendet.

Beim weglassen einer Personalnummer werden die Einzelnachweise von allen vorhandenen Mitarbeitern erzeugt und als Zip gepackt. Die ID des Anforders dient dazu, die Mailadresse aus der Datenbank in li_user rauszulesen und den Download link per Mail zu verschicken.

```python
python job.py MONAT JAHR ANFORDERER
```

Die Reports/Zip´s liegen im Ordner Reports im Überverzeichnis. D.h. der Ordner muss ggf. erste händisch angelegt werden. Gleiches gilt für den Ordner Logs.
Das versenden der Mail erfolgt über Zugangsdaten die in der config.ini angepasst werden müssen.


<img src=Pics/einzelnachweis_example.png alt="Einzelnachweis Beispiel" width="480">

Aus der Webapplikation kann dieser Report erzeugt werden. Hierfür den User im Modul Personaldaten raussuchen, Monat und Jahr wählen und PDF-Report klicken. Der Report wird zum Download angeboten.

<img src=Pics/einzelnachweis_web_example.png alt="Tagesreport Webansicht" width="480">

Im Falle zum Nachweisen aller Mitarbeiter ist dies unter dem Modul Reports zu finden. Hier kann ein Monatsreport für alle Mitarbeiter erstellt werden. Dabei werden die Einzelnachweise in ein Zip gepackt. Das Zip wird nicht direkt zum Download angeboten, je nach Anzahl der Mitarbeiter kann der Erstellungsvorgang mehrere Minuten dauern.
Der Downloadlink wird per Mail an den Anforderer versendet.

<img src=Pics/gesamtnachweis_web_example.png alt="Gesamtnachweis Webansicht" width="480">

### CSVExports
Der CSV Export dient zur Übersicht aller geleisteten Stunden der Mitarbeiter und der Ausgabe in dem für das Abrechnugssystem erwarteten Formats.
Das Format der CSV kann unter CSVExport/createCSV.py angepasst werden und ist Abrechnungsspezifisch. Der Output liegt ebenfalls im Ordner Reports.

Angestoßen wird die Erzeugung via der job.py mit der Übergabe von MONTA und Jahr als Argumente.

```python
python job.py MONAT JAHR
```

Aus der Webapplikation kann diese CSV ebenfalls erzeugt werden. Hierfür den Monat und das Jahr auswählen und auf CSV-Report klicken. Der Report wird zum Download angeboten.

<img src=Pics/abrechnung_web_example.png alt="Abrechnung Webansicht" width="480">