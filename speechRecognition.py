"""
ECE 5725 Fall 2021
Final Project

VoiceControlledGomoku
Zehua Pan(zp74) and Yuhao Lu(yl3539)

"""

# Global Python libraries
import sys
import time
import os
import speech_recognition as sr
import RPi.GPIO as gpio
import signal
from InputHandler import InputHandler

# Local Python modules
from recordAudio import RecordAudio
import globalParamters as gp

########################################
# global variables
########################################

# current file name
CUR_FILE = __file__.split("/")[-1]

# Quit btn
QUIT_BTN = 27

########### LED Indicator pin
#red LED - white peice 
LED_PIN_WHITE = 13
#green LED - black peice 
LED_PIN_BLACK = 17
# LED map
LED_map = {
    'White': LED_PIN_WHITE,
    'Black': LED_PIN_BLACK
    }
inputHandler = InputHandler('','')

########################################
# special events handling 
########################################

# close LED when program exit
def catchHandler(signum,frame):
    gpio.cleanup()
    print(f"[{CUR_FILE}] gpio cleaned")
    exit(1)

# physical callback function for exit
def GPIO27_callback(channel):
    gpio.cleanup()
    print(f'[{CUR_FILE}] gpio cleaned')
    os.system(f'echo "exit" > {gp.FIFO_USERIN}')
    exit(1)

def gpioSetUp():
    # Set up indicator LED
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN_WHITE, gpio.OUT)
    gpio.setup(LED_PIN_BLACK, gpio.OUT)
    gpio.setup(QUIT_BTN, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(27,gpio.FALLING,callback=GPIO27_callback,bouncetime=500)

########################################
# speech recognition progress handling 
########################################

def recognize(audioFile):
    # Initialize object instances
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audioFile)

    with audio as source:
        # Adjust for noise in the beginning
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        audio = recognizer.recordAudio(source)

        # Send the recognition request to Google 
        # Return None if no response
        try:
            res = recognizer.recognize_google(audio)
            print(f'[{CUR_FILE}] Found: ' + res)
            return res
        except:
            print(f'[{CUR_FILE}] Not found')
            return 'not found'

def getResult(microphone,color='White'):
    if(color not in LED_map):
        color = 'White'
    result  = ""
    # Indicate start of recording with LED and animation    
    gpio.output(LED_map[color], 1)
    # Record audio 
    microphone.record()
    # Indicate end of recording 
    gpio.output(LED_map[color], 0)
    # Recognize any speech in the recorded audio, if not found, return None
    audioFile = microphone.saveAudio()

    print(f"[{CUR_FILE}] Recognizing...")
    result = recognize(audioFile)
    # Delay before next recognition, time for thinking
    time.sleep(1)
    return result

def startRecognize():
    # FIFO will use the same path as current file
    FIFO_PATH = gp.FIFO_USERIN
    # Initialize objects for recognition
    microphone = RecordAudio()
    while True:
        # get LED color from Gomoku by FIFO
        LED_color = inputHandler.getLED()
        print(f"[{CUR_FILE}] Current LED color: {LED_color}")

        # Record and try recognizing voice userInput until any words detected
        print(f"[{CUR_FILE}] Tell me the position of your piece, format:[number-number]")
        userInput = getResult(microphone,LED_color)

        if userInput:
            # send userInput to fifo
            os.system(f'echo "{userInput}" > {FIFO_PATH}')
            if(userInput in gp.commandMap and gp.commandMap[userInput] == 'exit'):
                exit(1)
        else: 
            print(f"[{CUR_FILE}] Result: No")

if __name__ == "__main__":
    # set up gpio 
    gpioSetUp()
    # catch error
    signal.signal(signal.SIGINT, catchHandler)
    # recognize
    startRecognize()




