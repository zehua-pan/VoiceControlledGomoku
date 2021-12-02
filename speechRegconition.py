# Global Python libraries
import time
import os
import speech_recognition as sr
import RPi.GPIO as gpio
import signal
from InputHandler import InputHandler

# Local Python modules
from record import RecordAudio
import globalParamters as gp

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

# close LED when program exit
def catchHandler(signum,frame):
    gpio.cleanup()
    print("gpio cleaned")
    exit(1)


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
            print('[speech] Found: ' + res)
            return res
        except:
            print('[speech] Not found')
            return None

def getResult(mic,color='White'):
    if(not color):
        color = 'White'
    result  = ""
    print("[main] Recognizing...")
    # Indicate start of recording with LED and animation    
    gpio.output(LED_map[color], 1)
    # Record audio 
    mic.record()
    # Indicate end of recording 
    gpio.output(LED_map[color], 0)
    # Recognize any speech in the recorded audio, if not found, return None
    result = recognize(mic.save())
    # Delay of 2s before next recognition
    time.sleep(2)
    return result

def main():
    
    # catch error
    signal.signal(signal.SIGINT, catchHandler)

    FIFO_PATH = gp.FIFO_NAME
    # Initialize objects for recognition
    mic = RecordAudio()
    # Set up indicator LED
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN_WHITE, gpio.OUT)
    gpio.setup(LED_PIN_BLACK, gpio.OUT)
    while True:
        LED_color = inputHandler.getLED()
        # Record and try recognizing voice userInput until any words detected
        print("Tell me the position of your piece, format:[number-number]")
        userInput = getResult(mic,LED_color)
        if userInput:
            # send userInput to fifo
            os.system(f'echo "{userInput}" > {FIFO_PATH}')
        else: 
            print("[main] Result: None")

if __name__ == "__main__":
    main()




