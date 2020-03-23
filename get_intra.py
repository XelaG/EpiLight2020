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
from termcolor import colored
import pandas
from wrapper import intra_wrapper
from datetime import datetime
import time


def create_dictionary(filename):
    my_data = pandas.read_csv(filename, sep=',', index_col=False)
    list_of_dicts = [item for item in my_data.T.to_dict().values()]
    return list_of_dicts

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

def epiLight(intranet, data):
    while True:
        print(colored("NEW CHECK", 'blue'))
        for i in range(len(data)):
            is_room_taken = 0
            infos = intranet.get_room_info(data[i]["ROOM"])
            if infos == "error":
                print("Could not retrive room infos")
                continue
            for n in range(len(infos)):
                tmp = is_room_occupied(infos[n])
                if tmp >= is_room_taken:
                    is_room_taken = tmp
            if  is_room_taken == 1:
                print(colored("Room {} is occupied".format(data[i]["ROOM"]), 'red'), end=" ")
                print(colored("Sending RED ON to {}".format(data[i]["LED_IP"]), 'red'))
            elif is_room_taken == 2:
                print(colored("Room {} will be occupied in 30 minutes".format(data[i]["ROOM"]), 'yellow'), end=" ")
                print(colored("Sending YELLOW ON to {}".format(data[i]["LED_IP"]), 'yellow'))
            else:
                print(colored("Room {} is not occupied".format(data[i]["ROOM"]), 'green'), end=" ")
                print(colored("Sending GREEN ON to {}".format(data[i]["LED_IP"]), 'green'))
        time.sleep(300)

def main():
    args = []
    for arg in sys.argv:
        args.append(arg)
    intranet = intra_wrapper.intra(args[1])
    data = create_dictionary(args[2])
    epiLight(intranet, data)


main()