# Global Python libraries
import sys
import time
import os
import speech_recognition as sr
import RPi.GPIO as gpio
import signal
from InputHandler import InputHandler

# Local Python modules
from record import RecordAudio
import globalParamters as gp

CUR_FILE = __file__.split("/")[-1]

# quit btn
QUIT_BTN = 27

# LED Indicator pin
#red LED - white peice 
LED_PIN_WHITE = 13
#green LED - black peice 
LED_PIN_BLACK = 17
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

def recognize( audio ):
    # Initialize object instances
    rec = sr.Recognizer()
    audio = sr.AudioFile(audio)

    with audio as source:
        # Adjust for noise in the beginning 0.5 s
        rec.adjust_for_ambient_noise(source, duration=0.5)
        audio = rec.record(source)

        # Send the recognition request to Google 
        # Return None if no response
        try:
            res = rec.recognize_google(audio)
            print(f'[{CUR_FILE}] Found: ' + res)
            return res
        except:
            print(f'[{CUR_FILE}] Not found')
            return 'not found'

def getResult(mic,color='White'):
    if(color not in LED_map):
        color = 'White'
    result  = ""
    print(f"[{CUR_FILE}] Recognizing...")
    # Indicate start of recording with LED and animation    
    gpio.output(LED_map[color], 1)
    # Record audio 
    mic.record()
    # Indicate end of recording 
    gpio.output(LED_map[color], 0)
    # Recognize any speech in the recorded audio, if not found, return None
    result = recognize(mic.save())
    # Delay of 2s before next recognition
    time.sleep(1)
    return result

def main():
    # set up gpio 
    gpioSetUp()
    # catch error
    signal.signal(signal.SIGINT, catchHandler)

    FIFO_PATH = gp.FIFO_USERIN
    # Initialize objects for recognition
    mic = RecordAudio()
    while True:
        LED_color = inputHandler.getLED()
        print(f"[{CUR_FILE}] Current LED color: {LED_color}")
        # Record and try recognizing voice userInput until any words detected
        print(f"[{CUR_FILE}] Tell me the position of your piece, format:[number-number]")
        userInput = getResult(mic,LED_color)
        if userInput:
            # send userInput to fifo
            os.system(f'echo "{userInput}" > {FIFO_PATH}')
            if(userInput in gp.commandMap and gp.commandMap[userInput] == 'exit'):
                exit(1)
        else: 
            print(f"[{CUR_FILE}] Result: None")
        #  time.sleep(0.1)

if __name__ == "__main__":
    main()




