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

## Tagesreports
Der Tagesreport dient dazu, die Dienste des Vortages aufzulisten. Dies kann z.b. per Cron dem Schichtleiter zugesendet werden. Das Layout als Beispiel sieht wie folgt aus:

<img src=Pics/tagesreport_example.png alt="Server Disconnect" width="480">

Nachts werden via Konfiguration in phpmyadmin alle offenen Dienste automatisch geschlossen. Dies wird in der Spalte "AutoClose" auch markiert, so dass im Report die Zeiteinträge die vermutlich fehlerhaft sind farblich markiert werden.

Der nächtliche Autoclose wird konfiguriert mit:

```mysql
CREATE EVENT `Nightly AutoClose` ON SCHEDULE EVERY 23 DAY STARTS '2021-01-01 14:49:49' ENDS '2021-12-31 14:49:49' ON COMPLETION NOT PRESERVE ENABLE DO Update Dienste SET Dienstende = current_timestamp(), AutoClosed = '1' WHERE Dienstende is NULL
```

Das setzten der pdf kann unter Tagesreport/pdf.py angepasst werden. Ausführen der job.pdf ohne Argmente erzeugt einen Tagesreport des vergangenen Tages. Beim Übergaben eines Datums in der Form "YYYY-MM-DD" wird der Tagesreport für den übergebenen Tag erzeugt.

## Einzelabrechnungen

## CSVExports