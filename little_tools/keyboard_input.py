#%%
import pyautogui
import time 
heros = [20203,20510,20519,20520,20303]
level = 230
time.sleep(2)
for hero in heros:
    pyautogui.typewrite("setherolevel {hero} {level}\n".format(hero=hero,level=level))
    time.sleep(0.5)

    pyautogui.typewrite("setherostar {hero} 40\n".format(hero=hero))
    time.sleep(0.5)

# %%
