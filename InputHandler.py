import os
import errno
import globalParamters as gp

class InputHandler:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.msg = ''
        self.commandMap = {
            'exit': 'exit',
            'exit game': 'exit',
            'quit': 'exit',
            'quit game': 'exit',
            'quite': 'exit',
            'quite game': 'exit',
            'play again': 'again',
            'again': 'again',
        }

    def inBounds(self, row, col):
        return row >=0 and row < self.rows and col >= 0 and col < self.cols

    def getCoordinate(self, command):
        comList = command.split("-")
        return int(comList[0]), int(comList[1])

    def checkCommand(self, command):
        if(command in self.commandMap):
            self.msg = self.commandMap[command]
            return False
        comList = command.split("-")
        if(len(comList) != 2): 
            self.msg = "Try again : You need to command with [number]-[number]"
            return False
        if(not comList[0].isdigit() or not comList[1].isdigit()): 
            self.msg = "Try again : You need to command with [number]-[number]"
            return False
        row = int(comList[0])
        col = int(comList[1])
        if(not self.inBounds(row, col)): 
            print("Try again : The input integers are out of bound")
            self.msg = "Try again : The input integers are out of bound"
            return False
        self.msg = "Success : you made a move at {}-{}".format(row,col)
        print(self.msg)
        return True
    
    def getLED(self):
        command=""
        try:
            os.mkfifo(gp.FIFO_LED)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        # get command from fifo
        with open(gp.FIFO_LED) as fifo:
            command = fifo.read()
        if command[-1] == "\n" : command = command[:-1]
        return command

    def getCommand(self):
        command = ""
        userRow, userCol = "", ""
        isValid = False
        # create FIFO, ignore if exist
        try: 
            os.mkfifo(gp.FIFO_NAME)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
  
        # get command from fifo
        with open(gp.FIFO_NAME) as fifo:
            command = fifo.read()
        # remove the carriage return brought by file
        if command[-1] == "\n" : command = command[:-1]
        if(self.checkCommand(command)):
            isValid = True
            userRow, userCol = self.getCoordinate(command)
            

        return isValid, userRow, userCol, self.msg

