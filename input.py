import pyautogui
import pyperclip
import time
text = open("input.txt",'r')
time.sleep(5)
print("start")
for line in text:
    input("continue")
    l = line.replace("\n","")
    pyperclip.copy("additem {line} 2\n".format(line=l))
    print("additem {line} 2\n".format(line=l))
    # pyautogui.typewrite("additem {line} 2\n".format(line=l))
text.close()
print("finish")