""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Recorder for the Speech Recognition module.
Contains the RecordAudio class used to record and save audio 
snippets for speech recognition.
""" 

# Import global libraries
import pyaudio
import wave

# Define constants
SAMPLE_FORMAT = pyaudio.paInt16 # 16 bits per sample
FS = 44100 # Sampling rate

""" 
RecordAudio
Class to encapsulate an audio recording instance.

chunk: Number of samples in a chunk
channels: Number of channels
seconds: Duration of sound recording
filename: Output file
frames: Array to store frames
p: PyAudio instance
"""
class RecordAudio:
    """ 
    Constructor 
    """
    def __init__(s):
        s.chunk = 1024  # Record in chunks of 1024 samples
        s.channels = 1
        s.seconds = 3
        s.filename = "output.wav"
        s.frames = [] # Empty array to store frames

        s.p = pyaudio.PyAudio()  # Create an interface to PortAudio

    """ 
    record()
    Function to record s.seconds long audio and save samples in s.frames
    """
    def record(s):
        print('[record] Recording')
        # Initialize the stream object from PyAudio
        stream = s.p.open(format=SAMPLE_FORMAT,
                channels=s.channels,
                rate=FS,
                frames_per_buffer=s.chunk,
                input=True)

        # Store data in chunks for 3 seconds
        for i in range(0, int(FS / s.chunk * s.seconds)):
            data = stream.read(s.chunk)
            s.frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        print('[record] Finished recording')

    """ 
    save()
    Function to save the collected samples to s.filename

    Returns: Name of the file where samples stored
    """
    def save(s):
        # Save the recorded data as a WAV file
        wf = wave.open(s.filename, 'wb')
        wf.setnchannels(s.channels)
        wf.setsampwidth(s.p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(s.frames))
        wf.close()

        # Clear frames after writing
        s.frames = []

        return s.filename

