import numpy as np
import cv2


#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#def set():
	
def red():
	mask = cv2.inRange(img, lower_r, upper_r)
	#resR = cv2.bitwise_and(img,img, mask= maskR)
	#gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(mask, (5, 5), 0)
	contour, hierarchy =   cv2.findContours(blur,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("Image", mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return len(contour)

def green():
	mask = cv2.inRange(img, lower_g, upper_g)
	#resG = cv2.bitwise_and(img,img, mask= maskG)
	#gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(mask, (5, 5), 0)
	contour, hierarchy =   cv2.findContours(blur,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)	
	cv2.imshow("Image", mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows
	return len(contour)
	
def blue():
	mask = cv2.inRange(img, lower_b, upper_b)
	#resG = cv2.bitwise_and(img,img, mask= maskG)
	#gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(mask, (5, 5), 0)
	contour, hierarchy =   cv2.findContours(blur,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("Image", mask)
	cv2.waitKey(0)	
	cv2.destroyAllWindows()
	return len(contour)

	



#img = cv2.imread('shapes.png', 1)
#cv2.imshow('test', img)
img = cv2.imread('shapes.png', 1)
cv2.imshow('test', img)

lower_r = np.array([0, 0, 255])
upper_r = np.array([0, 0, 255])

lower_g = np.array([0, 255, 0])
upper_g = np.array([0,255, 0])


lower_b = np.array([255, 0, 0])
upper_b = np.array([255, 0, 0])
colorList = [0, 0, 0]
   


colorList[0] = red()
colorList[1] = green()
colorList[2] = blue()

print colorList
cv2.destroyAllWindows()
