# Global Python libraries
import subprocess
import time
import speech_recognition as sr
import RPi.GPIO as gpio

# Local Python modules
from record import RecordAudio
import speech

# LED Indicator pin
LED_PIN = 13

# Dictionary to store commands with their variations 
COMMANDS = {
    'GO': ['GO', 'GHOUL', 'GOOGLE', 'COOL'],
    'BACK': ['BACK', 'MATT', 'MAC'],
    'RIGHT': ['RIGHT', 'GOODNIGHT', 'DID I', 'TODAY', 'NIGHT', 'LIGHT'],
    'LEFT': ['LEFT', 'LAST', 'YES'],
    'GOOD': ['GOOD'],
    'LOOK': ['LOOK', 'YOLK'],
    'QUIT': ['QUIT', 'QUICK']
}

# List of no commands 
NO_COMMANDS = ['NONE', 'DONE']

""" 
recognize(rec, mic)
Helper function to record an audio snippet and send request to recognize. 

rec: Recognizer instance from SpeechRecognition library
mic: RecordAudio instance

Returns: Recognized speech (if any)
"""
def recognize(rec, mic):
    result  = ""
    print("[main] Recognizing...")

    # Indicate start of recording with LED and animation    
    gpio.output(LED_PIN, 1)
    # Send appropriate command to Animation module through FIFO
    subprocess.check_output('echo "1" > ../speechToAnimation.fifo', shell=True)
    subprocess.check_output('echo "1" >> ../speechToAnimation.log', shell=True)
    # Record audio 
    mic.record()
    # Indicate end of recording 
    gpio.output(LED_PIN, 0)
    subprocess.check_output('echo "2" > ../speechToAnimation.fifo', shell=True)
    subprocess.check_output('echo "2" >> ../speechToAnimation.log', shell=True)

    # Recognize any speech in the recorded audio
    result = speech.recognize(mic.save())
    # Delay of 2s before next recognition
    time.sleep(2)

    return result

"""
check(cmd)
Helper function to check if the recognized command is known 
by checking through the command and its variations. 

cmd: Command to check

Returns: Actual command from the variations, if any, else None
"""
def check(cmd):
    for key, val in COMMANDS.items():
        if cmd in val:
            return key
    
    return None

def main():
    #  # Before starting recognition, waits for response from the Ping script to check if
    #  # owner at home
    #  subprocess.call('sudo python3 ping.py', shell=True)
    #  # Indicate to animation that user found
    #  subprocess.check_output('echo "YAY" > ../speechToAnimation.fifo', shell=True)
    #  subprocess.check_output('echo "YAY" >> ../speechToAnimation.log', shell=True)

    # Initialize objects for recognition
    rec = sr.Recognizer()
    mic = RecordAudio()

    #  # Set up indicator LED
    #  gpio.setmode(gpio.BCM)
    #  gpio.setup(LED_PIN, gpio.OUT)
    
    while True:
        # Record and try recognizing voice command until any words detected
        print("[main] Please speak a command")
        command = None
        while command is None:
            command = recognize(rec, mic)

        print("[main] Result: " + command)

        #  # Check if the command detected is known
        #  command = command.upper()
        #  check_cmd = check(command.upper())

        #  # If in invalid commands, back to detection
        #  if command in NO_COMMANDS:
        #      continue
        
        #  if not check_cmd is None:
        #      # Known command
        #      print("[main] Command found: " + check_cmd)
        #      command = check_cmd
        #      # Existing command mode to Animation
        #      fifo_cmd = 'echo ' + command + ' > ../speechToAnimation.fifo'
        #      subprocess.check_output(fifo_cmd, shell=True)
        #      fifo_cmd = 'echo ' + command + ' >> ../speechToAnimation.log'
        #      subprocess.check_output(fifo_cmd, shell=True)
        #  else :
        #      # New command mode
        #      subprocess.check_output('echo "NEW" > ../speechToAnimation.fifo', shell=True)
        #      subprocess.check_output('echo "NEW" >> ../speechToAnimation.log', shell=True)
        #
        # Send the command to hand-detector module 
        fifo_cmd = 'echo ' + command + ' > ../speechToHand.fifo'
        subprocess.check_output(fifo_cmd, shell=True)
        fifo_cmd = 'echo ' + command + ' >> ../speechToHand.log'
        subprocess.check_output(fifo_cmd, shell=True)

        # Wait for acknowledgement from hand-detector
        hand_fifo = open('../handToSpeech.fifo', 'r')
        hand_cmd = hand_fifo.readline()[:-1]
        if not hand_cmd is "DONE" and not hand_cmd is "NONE":
            # If new command sent and received positive response from hand-detector
            # add the new command
            COMMANDS[hand_cmd] = [hand_cmd]

        # Send acknowledgment to animation to complete 
        subprocess.check_output('echo "DONE" >> ../speechToAnimation.log', shell=True)
        subprocess.check_output('echo "DONE" > ../speechToAnimation.fifo', shell=True)

        # Stop execution if Quit command
        if command == 'QUIT':
            running = False

if __name__ == "__main__":
    main()
