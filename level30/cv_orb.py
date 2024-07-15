#%%
import numpy as np
import cv2 as cv


img1 = cv.imread("yao.png")
img2 = cv.imread("template.png")

# orb = cv.ORB_create()
orb = cv.ORB.create()

kp1 = orb.detect(img1)
kp2 = orb.detect(img2)

kp1,des1 = orb.compute(img1,kp1)
kp2,des2 = orb.compute(img2,kp2)

outimg1 = cv.drawKeypoints(img1,keypoints=kp1,outImage=None)
outimg2 = cv.drawKeypoints(img2,keypoints=kp2,outImage=None)


bf = cv.BFMatcher(cv.NORM_HAMMING)

matches = bf.match(des1,des2)

min_distance = matches[0].distance
max_diatance = matches[0].distance
for x in matches:
    if x.distance < min_distance:
        min_distance = x.distance
    if x.distance > max_diatance:
        max_diatance = x.distance
good_match = []

def draw_match(img1,img2,kp1,kp2,match):
    outimage = cv.drawMatches(img1,kp1,img2,kp2,match,outImg=None)
    cv.imshow("Match Result",outimage)
    cv.waitKey(0)

for x in matches:
    if x.distance <= max(2 * min_distance,30):
        good_match.append(x)


draw_match(img1,img2,kp1,kp2,good_match)

# %%
