#%%
from adbutils import adb

ds = adb.device_list()

# d = adb.device(ds[0])
d = ds[0]
# d.shell("input motionevent 100 500")

d.shell("input motionevent DOWN 100 500")
for i in range(6):
    d.shell("input motionevent MOVE {x} 500".format(x=100+i*20))
d.shell("input motionevent UP 200 500")



#%%

import re

line = "/dev/input/event3: EV_KEY       BTN_TOUCH            UP"

info_serch = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}|ABS_MT_POSITION_Y +[0-9a-f]{8}|BTN_TOUCH +DOWN|BTN_TOUCH +UP',line)



# %%
