import sys

def dayInt_to_string(day):
    try:
        days = ("Empty","Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag")
        return days[day+1]
    except:
        return "Unknown"
