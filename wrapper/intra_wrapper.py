##
## EPITECH PROJECT, 2020
## epilight
## File description:
## intra_wrapper
##


from datetime import datetime
from urllib import request, parse
import json
import time

class intra(object):

    def __init__(self, token):
        self.token = token
        self.url = "https://intra.epitech.eu/"
        self.file_path = "data.json"
        self.last_update_time = 0
        self.planning_path = "planning/load?format=json"

    def refresh_data(self):
        date = datetime.now()
        self.last_update_time = date
        date = str(date)
        date = date.split()
        path = self.url + self.token + self.planning_path + "&start=" + date[0] + "&end=" + date[0]
        data = self.get_data(path)
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
        print("DATA REFRESHED")

    def get_data(self, path):
        res = request.urlopen(path)
        data = json.loads(res.read())
        return (data)

    def get_room_info(self, room_name):
        
        if self.last_update_time == 0:
            self.refresh_data()
        timediff = datetime.now() - self.last_update_time
        if timediff.total_seconds() > 3600:
            self.refresh_data()
        with open(self.file_path, 'r') as myfile:
            tmp = myfile.read()
        data = json.loads(tmp)
        list_of_dict = []
        for i in range(len(data)):
            if "room" not in data[i]:
                continue
            elif "code" not in data[i]["room"]:
                continue
            else:
                if data[i]["room"]["code"] == room_name:
                    stock = {'room_name' : data[i]["room"]["code"], 'start': data[i]["start"], 'end': data[i]["end"]}
                    list_of_dict.append(stock)
        return(list_of_dict)