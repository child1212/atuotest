#%%
import cv2 as cv
import os
import time
import matplotlib.pyplot as plt
import imghdr



def punch(dir):
    os.system("adb -e exec-out screencap -p > {dir}\\leidian.jpg".format(dir=dir))
    leidian = imghdr.what("{dir}\\leidian.jpg".format(dir=dir))
    if leidian == "png":
        imgs = ["l0.png","l1.png","l2.png","l3.png","l4.png","l5.png","r0.png","r1.png","r2.png","r3.png","r4.png","r5.png"]

        ans_l = []
        for imgpath in imgs:
            img = cv.imread(imgpath)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            w,h = gray.shape[::-1]
            img1 = cv.imread("{dir}\\leidian.jpg".format(dir=dir))
            gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
            if cv.minMaxLoc(match)[1]>0.985:
                ans_l.append(int(imgpath[1]))
        print(ans_l)
        ans = sum(ans_l)
        print(ans)
        img_ans = cv.imread("ans{ans}.png".format(ans=ans))
        gray_ans = cv.cvtColor(img_ans, cv.COLOR_BGR2GRAY)
        w,h = gray_ans.shape[::-1]
        match_ans = cv.matchTemplate(gray1,gray_ans,cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc =cv.minMaxLoc(match_ans)
        top_left = max_loc
        middle = (top_left[0] + w//2,top_left[1] + h//2)
        os.system("adb shell input tap {x} {y}".format(x=middle[0],y=middle[1]))

        time.sleep(1)
        return 0
    else:
        return 1


if __name__ == "__main__":
    dir = os.path.dirname(os.path.abspath(__file__))
    run = 0
    while run == 0:
        run = punch(dir)
    print("leidian.jpg is not exist, or damaged.\n请开启模拟器后重试。")
    input("press enter to exit!")
            





# %%
