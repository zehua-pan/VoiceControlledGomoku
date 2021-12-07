import os
import errno
import globalParamters as gp

class InputHandler:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.msg = ''
        self.operatorList = ["-", "*", "+", "/", "|", "="]
        self.cmdList = []

    def inBounds(self, row, col):
        return row >=0 and row < self.rows and col >= 0 and col < self.cols

    def getCoordinate(self, command):
        return int(self.comList[0]), int(self.comList[1])

    def commandParse(self, command):
        cmdList = []
        index = 0
        while len(cmdList) < 2 and index < len(self.operatorList):
            cmdList = command.split(self.operatorList[index])
            index += 1
        for i in range(len(cmdList)):
            cmdList[i] = cmdList[i].strip()
        for i in range(len(cmdList)):
            if(cmdList[i] == ""): cmdList.pop(i)
        return cmdList

    def checkCommand(self, command):
        # handle special command, if yes, return directly
        if(command in gp.commandMap):
            self.msg = gp.commandMap[command]
            return False
        self.comList = self.commandParse(command)

        # handle normal user inputs
        if(len(self.comList) != 2): 
            self.msg = "Try again : You need to command with [number]-[number]"
            return False
        if(not self.comList[0].isdigit() or not self.comList[1].isdigit()): 
            self.msg = "Try again : You need to command with [number]-[number]"
            return False
        row = int(self.comList[0])
        col = int(self.comList[1])
        if(not self.inBounds(row, col)): 
            print("Try again : The input integers are out of bound")
            self.msg = "Try again : The input integers are out of bound"
            return False
        self.msg = "Success : you made a move at {}-{}".format(row,col)
        print(self.msg)
        return True

    def handleFIFO(self, fifo_name):
        command = ""
        try:
            os.mkfifo(fifo_name)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        # get command from fifo
        with open(fifo_name) as fifo:
            command = fifo.read()
        if command != "" and command[-1] == "\n" : command = command[:-1]
        print(f"get command from {fifo_name}, command : {command}")
        return command

    def getLED(self):
        return self.handleFIFO(gp.FIFO_LED)

    def getCommand(self):
        userRow, userCol = "", ""
        isValid = False
        # create FIFO, ignore if exist
  
        command = self.handleFIFO(gp.FIFO_USERIN)
        if(self.checkCommand(command)):
            isValid = True
            userRow, userCol = self.getCoordinate(command)

        return isValid, userRow, userCol, self.msg.lower()

