import argparse
import paho.mqtt.client as mqtt
import os.path
import json
import time
import base64
import imghdr
from utils.constants import *

class Labelme2TB:
    def checkConfigFile(self, args):
        try:
            with open(args.file, 'rt') as file:
                data = json.load(file)
                if(data): 
                    return data
                else:
                    return 0
        except Exception as e:
             print('[ERROR] Invalid JSON file')
             print(e)

    def doiToaDo(points, h ,w):
        return [points[0][0]/w, points[0][1]/h]

    def getLabelList(label, data,name, h, w):
        l = []
        i = 1
        for item in data:
            if item['label'] == label:
                n = name+label+str(i)
                toado = doiToaDo(item['points'], h ,w)
                x = {"name": n, "label":n, "xPos": toado[0], "yPos": toado[1], "type": label}
                l.append(x)
                i +=1
        print(l)
        return l

    def run(self, original):
        data = checkConfigFile(args)
        name = args.name
        output = args.output
            
        genData = {}
        if(data):
            genData['Tang'] = name
            genData['ToaNha'] = "ThuVienTaQuangBuu"
            lBaoChay = getLabelList("BaoChay", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
            lBaoKhoi = getLabelList("BaoKhoi", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
            lPhunNuoc = getLabelList("PhunNuoc", data['shapes'], name, data['imageHeight'], data['imageWidth']) 
            genData['BaoChay'] = lBaoChay
            genData['BaoKhoi'] = lBaoKhoi
            genData['PhunNuoc'] = lPhunNuoc

        print(genData)
        with open(output + "/" + name +"_config.json", 'w') as f:
           json.dump(genData, f, indent=2) 