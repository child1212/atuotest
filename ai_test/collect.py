#%%
import uiautomator2 as u2
import json
import time

device = u2.connect()

def click(x,y,maxx,maxy,device):
    device.click(x/maxx,y/maxy)

def screenshot(path,device):
    device.screenshot(path)

def swipe(x1,y1,x2,y2,maxx,maxy,device):
    device.swipe(x1/maxx,y1/maxy,x2/maxx,y2/maxy,1)

dic={}
max_x = int(input("max_x:"))
max_y = int(input("max_y:"))
while True:
    act = input("action type(c,ci,s):")
    if act == "c":
        x = int(input("x:"))
        y = int(input("y:"))
        img_name = "{t}-click.jpg".format(t=int(time.time()*10)-17630200000)
        img_path = "D:\\screenshot\\"
        screenshot(img_path+img_name,device)
        click(x,y,max_x,max_y,device)
        dic = {
                "image": img_name,
                "action": {
                    "type": "tap",          
                    "x": x/max_x,                     
                    "y": y/max_y                      
                }
            }
    elif act == "ci":
        x = int(input("x:"))
        y = int(input("y:"))
        img_name = "{t}-click.jpg".format(t=int(time.time()*10)-17630200000)
        img_path = "D:\\screenshot\\"
        screenshot(img_path+img_name,device)
        click(x,y,max_x,max_y,device)
        dic = {
                "image": img_name,
                "action": [{
                    "type": "tap",          
                    "x": x/max_x,                     
                    "y": y/max_y                      
                },
                {
                    "type": "send_keys",          
                }]
            }
    elif act == "s":
        x = int(input("x1:"))
        y = int(input("y1:"))
        x2 = int(input("x2:"))
        y2 = int(input("y2:"))
        img_name = "{t}-swipe.jpg".format(t=int(time.time()*10)-17630200000)
        img_path = "D:\\screenshot\\"
        screenshot(img_path+img_name,device)
        swipe(x,y,x2,y2,max_x,max_y,device)
        dic = {
                "image": img_name,
                "action": {
                    "type": "swipe",          
                    "x1": x/max_x,                     
                    "y1": y/max_y,      
                    "x2": x2/max_x,                     
                    "y2": y2/max_y      
                }
            }
    elif act == 'q':
        break
    
    with open('file.json','r') as file:
        a = json.load(file)
    a.append(dic)
    with open('file.json','w') as file:
        json.dump(a,file)


