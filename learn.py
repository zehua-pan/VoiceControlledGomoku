import sys

command = ""
fifo_name = "FIFO_LED"
with open(fifo_name) as fifo:
    command = fifo.read()
if command[-1] == "\n" : command = command[:-1]
print(f"get command from {fifo_name}, command : {command}")

