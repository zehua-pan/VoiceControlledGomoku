import os
import errno
import globalParamters as gp

class InputHandler:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def inBounds(self, row, col):
        return row >=0 and row < self.rows and col >= 0 and col < self.cols

    def getCoordinate(self, command):
        comList = command.split("-")
        return int(comList[0]), int(comList[1])

    def checkCommand(self, command):
        comList = command.split("-")
        if(len(comList) != 2): 
            print("Try again : You need to input two numbers")
            return False
        if(not comList[0].isdigit() or not comList[1].isdigit()): 
            print("Try again : You need to input two integers")
            return False
        row = int(comList[0])
        col = int(comList[1])
        if(not self.inBounds(row, col)): 
            print(f"Try again : The input integers are out of bound")
            return False
        return True

    def getCommand(self):
        command = ""
        userRow, userCol = "", ""
        # create FIFO, ignore if exist
        try: 
            os.mkfifo(gp.FIFO_NAME)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        while True:
            # get command from fifo
            with open(gp.FIFO_NAME) as fifo:
                command = fifo.read()
            # remove the carriage return brought by file
            if command[-1] == "\n" : command = command[:-1]
            if(self.checkCommand(command)):
                userRow, userCol = self.getCoordinate(command)
                break
        return userRow, userCol

