#!/bin/python3

import requests
import bs4
import json
import html
import datetime

def fetchSubjects() -> str:

    groups = {"a1","lab2", "MAT3", "FN1", "čj1", "hst1", "CAE1", "ReGB", "ReGP", "LINV", "LINM", "HV", "Chl", ""}
    
    weekday_index : dict = {'po': 0, 'út': 1, 'st': 2, 'čt': 3, 'pá': 4}

    subject_abbreviations : dict = {
        "Biologie" : "Bi",
        "Český jazyk a literatura" : "Čj",
        "Humanitní studia" : "HSt",
        "Fyzika" : "Fy",
        "Anglický jazyk" : "Aj",
        "Francouzský jazyk" : "Fj",
        "Matematika" : "M",
        "Kurz přípravy CAE" : "CAEK",
        "Dějepis" : "Děj",
        "Regionální geografie" : "ReGe",
        "Hudební výchova" : "HV",
        "Chemie" : "Ch",
        "Linuxový seminář" : "Lin",
        "Tělesná výchova" : "TV"
    }

    table = [[] for _ in range(5)]

    r = requests.get('https://gjk.bakalari.cz/Timetable/Public/Actual/Class/20')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    for div in soup.select('div.day-item-hover[data-detail]'):
        data_detail_raw = div.get("data-detail", "")

        if not isinstance(data_detail_raw, str):
            continue

        data_detail_decoded = html.unescape(data_detail_raw)

        try:
            data = json.loads(data_detail_decoded)
            subject = data.get("subjecttext", "")
            if not subject: continue

            subject_items = subject.split(" | ")
            weekday_name = subject_items[1][:2]
            room = data.get("room", "")
            group = data.get("group", "")
            if  ( group in groups):
                table[weekday_index[weekday_name]].append(subject_abbreviations[subject_items[0]] + ' ' + room)
        except json.JSONDecodeError as e:
                print("JSON decode error:", e)

    return( "\n".join([ "; ".join(i) for i in table ]) )

def updateTimetable() -> None:
    outfile = open("/home/j/.local/share/rozvrh/timetable", "w")
    outfile.write( str( datetime.date.today().isocalendar()[1] ) + "\n" )
    outfile.close()
    outfile = open("/home/j/.local/share/rozvrh/timetable", "a")
    outfile.write( fetchSubjects() )
    outfile.close()
