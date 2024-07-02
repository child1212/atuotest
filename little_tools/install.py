#%%
from adbutils import adb
import threading

# p = input("path")
p = "\\\\10.12.3.92\\mgQA\\Test_File\\诛仙\\laohu_Game_2.838.1_202404172307_zs_4.7.5_30_signed.apk"
ds = adb.device_list()
i =100
for d in ds:
    r = adb.device(d.serial)
    # d.install(p)
    threading.Thread(target=r.install,args=(p,)).start()
    # r.shell("input text wmmw{t}@laohu.com".format(t=i))
    # r.shell("input text wmmw{t}pwrd".format(t=i))

    i += 1


