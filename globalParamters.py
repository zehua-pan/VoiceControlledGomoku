"""
ECE 5725 Fall 2021
Final Project

VoiceControlledGomoku
Zehua Pan(zp74) and Yuhao Lu(yl3539)

"""

FIFO_USERIN = "FIFO_USERIN"
FIFO_LED    = 'FIFO_LED'
commandMap = {
   'exit': 'exit', 
   'exit game': 'exit', 
   'quit': 'exit',
   'quit game': 'exit',
   'quite': 'exit',
   'quite game': 'exit',
   'play again': 'again',
   'again': 'again',
   'restart': 'again',
}

