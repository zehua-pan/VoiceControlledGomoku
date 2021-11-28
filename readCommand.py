import os
import errno

FIFO = "myFIFO"

# create FIFO, ignore if exist
print("Create FIFO")
try: 
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

#  while True:
#      print("Waiting for input to FIFO...")
#      with open(FIFO) as fifo:
#          print("FIFO opened")
#          command = fifo.read()
#          print(f"command : {command}")
#      print("FIFO closed\n")
#

fifo_file = open(FIFO, 'r')
command = fifo_file.readline()[:-1]
print(f"command : {command}")
