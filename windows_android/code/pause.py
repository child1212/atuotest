#%%
from tkinter import *

top = Tk()



top.title("autoclick")

top.geometry("400x200")

textExample = Text(top,height=10)

textExample.pack()

def getTextInput():
    result = textExample.get("1.0","end")
    top.quit()
    print(result)


btnRead = Button(top,height=1,width=10,text="Read",command=getTextInput)

btnRead.pack()

top.mainloop()
# %%
