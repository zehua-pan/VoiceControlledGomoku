# Global Python libraries
import time
import os
import speech_recognition as sr

# Local Python modules
from record import RecordAudio
import globalParamters as gp


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

def getResult(mic):
    result  = ""
    print("[main] Recognizing...")
    # Record audio 
    mic.record()
    # Recognize any speech in the recorded audio, if not found, return None
    result = recognize(mic.save())
    # Delay of 2s before next recognition
    time.sleep(2)
    return result

def main():
    FIFO_PATH = gp.FIFO_NAME
    # Initialize objects for recognition
    mic = RecordAudio()
    while True:
        # Record and try recognizing voice userInput until any words detected
        print("Tell me the position of your piece, format:[number-number]")
        userInput = getResult(mic)
        if userInput:
            # send userInput to fifo
            os.system(f'echo "{userInput}" > {FIFO_PATH}')
        else: 
            print("[main] Result: None")

if __name__ == "__main__":
    main()




