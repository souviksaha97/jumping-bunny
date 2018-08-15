#import numpy as np
import cv2
import math
import operator

#Grayscale threshold for RGBY
rgOfCol=	[
	(76,80),
	(149,150),
	(29,30),	
	(224,228)
]


container_objects = []
board_objects = []
output_list = []
boardDetails = []
contDetails = []


#returns the number of sides of the shape who's contour value is passed
def shape(cnt):
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.041 * peri, True)
	if len(approx) == 3:
		return "Triangle"
	elif len(approx) == 4:
		return "4-sided"
	else:
		return "Circle"	

#masks the board based on colour and selects each shape one by one, finds contours and calls shape(cnt) to find the shape
def colorSeg(path, dim):
	#Convt to grayscale and blur
	img = cv2.imread(path, 1) 
	imgGr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlr = cv2.medianBlur(imgGr, 3)
	imgFinBlr = cv2.GaussianBlur(imgBlr, (5, 5), 0)
	list1 = []
	details =[]
	i = 0; 
	k = 50.0 + (dim-1)*100.0
	while (i < 4):
		mask = cv2.inRange(imgFinBlr, rgOfCol[i][0], rgOfCol[i][1])
		blur = cv2.medianBlur(mask, 7)
		#tmp = cv2.medianBlur(mask, 7)

		contour, hierarchy =   cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		j = 0
		while (j < len(contour)):
			cnt = contour[j]
			M = cv2.moments(cnt)
			cx = int((M["m10"] / M["m00"]))
			cy = int((M["m01"] / M["m00"]))

			noOfSide = shape(cnt)

			if i == 0:
				color = "Red"
			elif i == 1:
				color = "Green"
			elif i == 2:
				color = "Blue"
			elif i == 3:	
				color = "Yellow"

			xCoord = math.ceil(dim*cx/k) if (math.ceil(dim*cx/k) <=dim) else round(dim*cx/k)
			yCoord = math.ceil(dim*cy/k) if (math.ceil(dim*cy/k) <=dim) else round(dim*cy/k)
			position = 0
			position = int(xCoord + (dim*(yCoord-1)))
			tupleElement = (position, color, noOfSide)
			tupleElement1 = (position, int(cv2.arcLength(cnt, True)), cv2.contourArea(cnt))
			details.append(tupleElement1)
			list1.append(tupleElement)
			j = j+1
		i=i+1
	list1.sort(key = operator.itemgetter(1,2))
	details.sort(key = operator.itemgetter(0))
	return list1, details

def matching():
	
	output = []
	i = 0
	j = 0
	c = 0
	while (i < len(boardDetails)):
		c = 0
		j = 0
		while (j < len(contDetails)):
			if ((abs(boardDetails[i][1]-contDetails[j][1]) <= 4) and (board_objects[i][1] == container_objects[j][1])):
				c = 1
				output.append((i+1, j+1))
				break

			j = j+1

		if (c == 0):
			output.append((i+1, 0))

		i = i+1



	return output

board_filepath = "board_6.jpg"
container_filepath = "container_3.jpg"

board_objects, boardDetails = colorSeg(board_filepath, 3)

container_objects, contDetails = colorSeg(container_filepath, 4)
output_list  = matching()

print board_objects, output_list

