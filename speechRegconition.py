# Global Python libraries
import time
import speech_recognition as sr

# Local Python modules
from record import RecordAudio

class

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
    # Initialize objects for recognition
    mic = RecordAudio()
    while True:
        # Record and try recognizing voice command until any words detected
        print("[main] Please speak a command")
        command = getResult(mic)
        if command:
            print("[main] Result: " + command)
        else: 
            print("[main] Result: None")

if __name__ == "__main__":
    main()




