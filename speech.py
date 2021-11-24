""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Speech recognizer function for the speech recognition module.
""" 
import speech_recognition as sr

""" 
recognize(audio)
Function to send request for speech recognition of the input audio file.

audio: File name of the audio

Returns: Result of recognition; text if found, else None
""" 
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
