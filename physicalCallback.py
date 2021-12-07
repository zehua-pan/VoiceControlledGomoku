import RPi.GPIO as GPIO
import time
import os
import subprocess
import globalParamters.py as gp
    |   |
button_num = [27]
size = len(button_num)
umap = {
    |   27:"quit"
    |   }

GPIO.setmode(GPIO.BCM)

for i in range(size):
    GPIO.setup(button_num[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def func(num):
    print("Button {} has been pressed".format(num))
    Gomoku_cmd = 'echo {} > {}'.format(umap[num], gp.FIFO_USERIN)
    speechRecognition_cmd = 'echo {} > {}'.format(umap[num], gp.FIFO_LED)
    os.system(Gomoku_cmd)
    os.system(speechRecognition_cmd)

def GPIO27_callback(channel):
    func(27)

btime = 600
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=btime)


