#%%
import cv2 as cv
import os
import time
import matplotlib.pyplot as plt
import imghdr
hand_set = {"l0.png","l1.png","l2.png","l3.png","l4.png","l5.png","r1.png","r2.png","r3.png","r4.png","r5.png"}

imgpath = 'go.png'

img = cv.imread(imgpath)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
w,h = gray.shape[::-1]
img1 = cv.imread("template.png")
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
if cv.minMaxLoc(match)[1]>0.95:
    match_ans = cv.matchTemplate(gray1,gray,cv.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc =cv.minMaxLoc(match_ans)
top_left = max_loc
middle = (top_left[0] + w//2,top_left[1] + h//2)
bottom_right = (top_left[0] + w,top_left[1] + h)

cv.rectangle(img1,top_left, bottom_right, 255, 2)
plt.subplot(121),plt.imshow(match,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img1,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.show()