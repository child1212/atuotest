#%%
import tkinter

def over():
    print(v.get())


window = tkinter.Tk()

window.title("Window")

a_dist = []

for i in range(10):
    a_dist.append((i,i))

v = tkinter.StringVar()

v.set("")

for x,y in a_dist:
    tkinter.Radiobutton(window,text=x,variable=v,value=y).pack()

btn = tkinter.Button(window,text="ok",command=over)
btn.pack()

window.mainloop()



# %%
