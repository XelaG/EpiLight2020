#!/usr/bin/env python3
##
## EPITECH PROJECT, 2020
## epilight
## File description:
## get_intra
##

from urllib import request, parse
import json
import sys
import serial
import enum
from termcolor import colored
import pandas
from wrapper import intra_wrapper
from datetime import datetime
import time

class Color(enum.Enum):
    green = 0
    yellow = 1
    red = 2

def create_dictionary(filename):
    while True:
        try:
            with open(filename, 'r') as myfile:
                tmp = myfile.read()
            break
        except EnvironmentError:
            print("Could not open file")
            filename = input("Please enter correct filepath : ")
    parsed_json = json.loads(tmp)
    return (parsed_json)

def time_to_sec(time):
    time = str(time)
    time = time.split(':')
    seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    return (seconds)

def is_hour_between_start_end(hour_checked, start, end, offset):
    start = start.split()
    end = end.split()
    hour_checked = time_to_sec(hour_checked)
    start = time_to_sec(start[1]) - offset
    end = time_to_sec(end[1]) - offset
    if hour_checked < end and hour_checked > start:
        return (True)
    else:
        return (False)

def is_room_occupied(infos):
    date = datetime.now()
    tmp = str(date)
    tmp = tmp.split()
    tmp2 = infos["start"].split()
    tmp3 = tmp[1].split('.')
    if tmp2[0] == tmp[0]:
        if is_hour_between_start_end(tmp3[0], infos["start"], infos["end"], 0) == True:
            return(1)
        if is_hour_between_start_end(tmp3[0], infos["start"], infos["end"], 1800) == True:
            return (2)
    return (0)

def sendOn(color, item):
    for i in range(len(item[1]["esp_uuids"])):
        print(colored("Send {} to ESP {} for room {}".format(color.name, item[1]["esp_uuids"][i], item[0]), color.name))

def epiLight(intranet, data):
    while True:
        print(colored("NEW CHECK", 'blue'))
        for item in data.items():
            is_room_taken = 0
            for i in range(len(item[1]["rooms"])):
                infos = intranet.get_room_info(item[1]["rooms"][i])
                if infos == "error":
                    print("Could not retrieve room infos")
                    continue
                for n in range(len(infos)):
                    tmp = is_room_occupied(infos[n])
                    if tmp > is_room_taken:
                        is_room_taken = tmp
                if i == len(item[1]["rooms"]) - 1:
                    if  is_room_taken == 1:
                        sendOn(Color.red, item)
                    elif is_room_taken == 2:
                        sendOn(Color.yellow, item)
                    else:
                        sendOn(Color.green, item)
        time.sleep(300)

def main():
    args = []
    for arg in sys.argv:
        args.append(arg)
    intranet = intra_wrapper.intra(args[1])
    data = create_dictionary(args[2])
    epiLight(intranet, data)


main()