#!/bin/python3

import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', action='store_const', const = True)

wd = datetime.date.today().weekday()
if wd in {5, 6}:
    quit()
infile = open("/home/j/.local/share/rozvrh/timetable", "r")
wd_timetables = infile.read().split('\n')
infile.close()

if datetime.date.today().isocalendar()[1] != int(wd_timetables[0]) or parser.parse_args().u:
    from scrape import updateTimetable
    updateTimetable()
    infile = open("/home/j/.local/share/rozvrh/timetable", "r")
    wd_timetables = infile.read().split('\n')
    infile.close()

print(wd_timetables[wd + 1])
