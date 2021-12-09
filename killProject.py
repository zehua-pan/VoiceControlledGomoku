import subprocess
import os

subpro = subprocess.Popen(['ps', '-af'], stdout=subprocess.PIPE)
output, error = subpro.communicate()

target1 = "speechRecognition.py"
target2 = "playGomoku.py"

for line in output.splitlines():
    text = str(line)
    if target1 in text or target2 in text:
        textList = text.split(" ")
        index = 1
        while(textList[index] == ""): index += 1
        pid = int(textList[index])
        os.kill(pid, 9)
