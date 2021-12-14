""" 
ECE 5725 Fall 2021
Final Project

VoiceControlledGomoku
Zehua Pan(zp74) and Yuhao Lu(yl3539)

""" 

import pyaudio
import wave

# get the current file name
CUR_FILE = __file__.split("/")[-1]

""" 
Class to encapsulate audio recording
"""
class RecordAudio:
    def __init__(self, timeForRecording=4):
        self.sampleRate = 44100 # Sampling rate
        self.sampleFormat = pyaudio.paInt16  
        self.chunk = 1024  # One chunk has 1024 samples
        self.channels = 1  
        self.seconds = timeForRecording # time for recording, see default value in the parameter lists
        self.filename = "humanAudio.wav"  # save file name for recognizing
        self.frames = [] # Empty array to store frames
        self.paudio = pyaudio.PyAudio()  # Create an instance of PortAudio

    """ 
    record s.seconds long audio and save it in s.frames
    """
    def recordAudio(self):
        print(f'[{CUR_FILE}] Recording')

        # Initialize the stream object from PyAudio
        stream = self.paudio.open(format=self.sampleFormat,
                                  channels=self.channels,
                                  rate=self.sampleRate,
                                  frames_per_buffer=s.chunk,
                                  input=True)

        # Reset frames before use
        self.frames = []

        # Store data in chunks for s.seconds
        # read one chunk at a time
        chunkNum = int((self.sampleRate / self.chunk) * self.seconds)
        for _ in range(chunkNum):
            data = stream.read(self.chunk)
            self.frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        print(f'[{CUR_FILE}] Finished recording')

    """ 
    save the collected samples to s.filename
    """
    def saveAudio(self):
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.paudio.get_sample_size(self.sampleFormat))
        wf.setframerate(self.sampleRate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        return self.filename

