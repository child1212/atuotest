#%%
import adbutils
import scrcpy
import cv2
import scrcpy_ui
import scrcpy_ui.ui_main


# scrcpy_ui.main()

scrcpy_ui.main()
# adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

# devices = adb.device_list()

# # print(d.shell("wm size"))

# client = scrcpy.Client(devices[0])

# def on_frame(frame):
#     if frame is not None:
#         cv2.waitKey(10)

# client.add_listener(scrcpy.EVENT_FRAME,on_frame)

# def on_init():
#     print(client.device_name)

# client.add_listener(scrcpy.EVENT_INIT,on_init)

# client.start(threaded=True)

# client.control.touch(500,500,scrcpy.ACTION_DOWN)

# client.control.touch(500,500,scrcpy.ACTION_UP)




















# %%
# from adbutils import adb


# adb.device_list()
# d = adb.device("2f20296")
# d.shell("input tap 906 1113")



# %%
