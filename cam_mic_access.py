import time
import cv2
import datetime as dt

from variables import *

def take_pic():
        TimeStamp = str(dt.datetime.now())
        camera = cv2.VideoCapture(0)
        time.sleep(0.1)
        cv2.imwrite(PROJECTROOT + "tmp/" + TimeStamp + ".png", camera.read()[1])
        del camera
        
        return ("Photo taken at {}".format(TimeStamp), open(PROJECTROOT + "tmp/" + TimeStamp + ".png","rb"))
