""" 
ECE 5725 Fall 2021
Final Project

VoiceControlledGomoku
Zehua Pan(zp74) and Yuhao Lu(yl3539)

""" 

import pyaudio
import wave

""" 
Class to encapsulate audio recording
"""
class RecordAudio:
    def __init__(s, timeForRecording=3):
        s.sampleRate = 44100 # Sampling rate
        s.sampleFormat = pyaudio.paInt16
        s.chunk = 1024  # One chunk has 1024 samples
        s.channels = 1  
        s.seconds = timeForRecording # time for recording
        s.filename = "output.wav"  # save file name for recognizing
        s.frames = [] # Empty array to store frames
        s.paudio = pyaudio.PyAudio()  # Create an interface to PortAudio

    """ 
    record s.seconds long audio and save it in s.frames
    """
    def record(s):
        print('Recording')
        # Initialize the stream object from PyAudio
        stream = s.paudio.open(format=s.sampleFormat,
                channels=s.channels,
                rate=s.sampleRate,
                frames_per_buffer=s.chunk,
                input=True)

        # Store data in chunks for 3 seconds
        # read one chunk at a time
        chunkNum = int((s.sampleRate / s.chunk) * s.seconds)
        for i in range(0, chunkNum):
            data = stream.read(s.chunk)
            s.frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        print('Finished recording')

    """ 
    save the collected samples to s.filename
    """
    def save(s):
        # Save the recorded data as a WAV file
        wf = wave.open(s.filename, 'wb')
        wf.setnchannels(s.channels)
        wf.setsampwidth(s.paudio.get_sample_size(s.sampleFormat))
        wf.setframerate(s.sampleRate)
        wf.writeframes(b''.join(s.frames))
        wf.close()

        # Clear frames after writing
        s.frames = []

        return s.filename

