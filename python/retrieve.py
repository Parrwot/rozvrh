#!/bin/python3

import datetime

wd = datetime.date.today().weekday()
if wd in {5, 6}:
    quit()
infile = open("/home/j/.local/share/rozvrh/timetable", "r")
wd_timetables = infile.read().split('\n')
infile.close()

if datetime.date.today().isocalendar()[1] != int(wd_timetables[0]):
    from scrape import updateTimetable
    updateTimetable()
    infile = open("/home/j/.local/share/rozvrh/timetable", "r")
    wd_timetables = infile.read().split('\n')
    infile.close()

print(wd_timetables[wd + 1])
