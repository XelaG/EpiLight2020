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
    hour_checked = time_to_sec(hour_checked) - offset
    start = time_to_sec(start[1])
    end = time_to_sec(end[1])
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
    if tmp2[0] == tmp2[0]:
        if is_hour_between_start_end(tmp3[0], infos["start"], infos["end"], 0) == True:
            return(1)
        if is_hour_between_start_end(tmp3[0], infos["start"], infos["end"], 1800):
            return (2)
    return (0)

def epiLight(intranet, data):
    while True:
        for i in range(len(data)):
            infos = intranet.get_room_info(data[i]["ROOM"])
            for n in range(len(infos)):
                is_room_taken = is_room_occupied(infos[n])
                if  is_room_taken == 1:
                    print("Room {} is occupied".format(infos[n]["room_name"]))
                    break
                elif is_room_taken == 2:
                    print("Room {} wille be occupied in 30 minutes".format(infos[n]["room_name"]))
                    break
                else:
                    print("Room {} is not occupied".format(infos[n]["room_name"]))
        time.sleep(300)

def main():
    args = []
    for arg in sys.argv:
        args.append(arg)
    intranet = intra_wrapper.intra(args[1])
    data = create_dictionary(args[2])
    epiLight(intranet, data)


main()