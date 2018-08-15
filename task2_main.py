# -*- coding: utf-8 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
* ---------------------------------------------------
*  Theme: Launch a Module
*  Filename: task2_main.py
*  Version: 1.0.0  
*  Date: November 28, 2016
*  How to run this file: python task2_main.py
*  Author: e-Yantra Project, Department of Computer Science and Engineering, Indian Institute of Technology Bombay.
* ---------------------------------------------------

* ====================== GENERAL Instruction =======================
* 1. Check for "DO NOT EDIT" tags - make sure you do not change function name of main().
* 2. Return should be a list named occupied_grids and a dictionary named planned_path.
* 3. Do not keep uncessary print statement, imshow() functions in final submission that you submit
* 4. Do not change the file name
* 5. Your Program will be tested through code test suite designed and graded based on number of test cases passed 
**************************************************************************
'''

'''
* Team ID: LM#3709
* Author List  		:Mihir Lele, Souvik Saha, Shivam Mahadeshwar, Sadiq Mujawar
* File name    		:task2_main.py
* Theme 	   		:Launch a Module
* Functions    		:dijkstra_search(graph, start, goal), reconstruct_path(came_from, start, goal), main_traverse(graph, source, destination), shape(int), colorSeg(path, int),
 						makeGrid(list, list), createPath(list, list), removeObstacles(), match()
* Global VARIABLES  : rgOfCol[], fullGridInfo, objectList[], occupied_grids[], planned_path{}

'''
# Algorithm used - Dijkstra 


import cv2
import numpy as np
import math
import operator
import heapq

# ******* WRITE YOUR FUNCTION, VARIABLES etc HERE
rgOfCol=	[(76, 80),(149, 150),(29, 30),(0, 10)] #RGBBl  R = 1, G = 2, B = 3, Obs = 4, Empty = 0
fullGridInfo = np.zeros((3,10,10))  #Color, shape, peri
objectList = []			# List of all the objects with color, shape, size, coordinates
occupied_grids = []		# List to store coordinates of occupied grid -- DO NOT CHANGE VARIABLE NAME
planned_path = {}		# Dictionary to store information regarding path planning  	-- DO NOT CHANGE VARIABLE NAME

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

# Grid Representation
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.weights = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

# Dijkstra Main Search
'''
* Function name  :  dijkstra_search
* Inputs		 :	graph, tuple, tuple
* Returns        : 	dictionary of path travelled and cost
* Logic          :	Uses djikstra algorithm to travel from start to goal
* Example Call   :  came_from, cost_so_far = dijkstra_search(graph, source, destination)
'''
def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

# Path Generation
'''
* Function name  :  reconstruct_path
* Inputs		 :	dictionary, tuple, tuple
* Returns        : 	List of tuples of path it travels
* Logic          :	Traverses from the end to the start of dictionary came_from,
					 until it reaches the start and appends tuples of coordinates travelled to path
* Example Call   :  path=reconstruct_path(came_from, start=source, goal=destination)
'''
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []

    while came_from[current] != start:
        current = came_from[current]
        path.append((current[0] + 1, current[1] + 1))

    path.reverse() 
    return path

# Main driver method for Dijkstra
'''
* Function name  :  main_traverse
* Inputs		 :	object of Grid, tuple, tuple
* Returns        : 	Dictionary of the answer in specified format
* Logic          :	Calls the necessary functions to do the Dijkstra Search
* Example Call   :  main_traverse(graph, source, destination)
'''
def main_traverse(graph, source, destination):
    came_from, cost_so_far = dijkstra_search(graph, source, destination)
    ans = {}

    try:
    	path=reconstruct_path(came_from, start=source, goal=destination)
    except KeyError:
    	ans[(source[0]+1, source[1]+1)] = "NO PATH", [], 0
    else:
    	ans[(source[0]+1, source[1]+1)] = (destination[0]+1, destination[1]+1),path,(len(path)+1)

    return ans

#returns the number of sides of the shape who's contour value is passed
'''
* Function name  :  shape
* Inputs		 :	contours
* Returns        : 	Number of sides of the shape given by the contour passed
* Logic          :	uses cv2.approxPolyDP to determine the number of sides
* Example Call   :  noOfSides = shape(cnt)
'''
def shape(cnt):
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.041 * peri, True)
	if len(approx) <=4:
		return len(approx)
	else:
		 return 5
'''
* Function name  :  colorSeg
* Inputs		 :	pathname, dimensions of the square in the grid
* Returns        : 	Fills in the data for occupied_grids and fullGridInfo
* Logic          :	Reads image, converts to greyscale, blurs and masks in order to get details of the color of the shapes
* Example Call   :  colorSeg(path, 10)
'''
def colorSeg(path, dim):
	#Convt to grayscale and blur
	img = cv2.imread(path, 1) 
	imgGr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlr = cv2.medianBlur(imgGr, 3)
	imgFinBlr = cv2.GaussianBlur(imgBlr, (5, 5), 0)
	i = 0; 
	k = 30.0 + (dim-1)*60.0
	while (i < 4):
		mask = cv2.inRange(imgFinBlr, rgOfCol[i][0], rgOfCol[i][1])
		blur = cv2.medianBlur(mask, 7)
		#tmp = cv2.medianBlur(mask, 7)

		contour, hierarchy =   cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(blur, contour, -1, (0,0,0), 1)
		j = 0
		while (j < len(contour)):
			cnt = contour[j]
			M = cv2.moments(cnt)
			cx = int((M["m10"] / M["m00"]))
			cy = int((M["m01"] / M["m00"]))
			peri = int(cv2.arcLength(cnt, True))

			noOfSide = shape(cnt)


			xCoord = math.ceil(dim*cx/k) if (math.ceil(dim*cx/k) <=dim) else round(dim*cx/k)
			yCoord = math.ceil(dim*cy/k) if (math.ceil(dim*cy/k) <=dim) else round(dim*cy/k)

			if (i!=4):
				occupied_grids.append((int(xCoord), int(yCoord)))

			fullGridInfo[0][int(yCoord)-1][int(xCoord)-1] = (i+1) #Color
			fullGridInfo[1][int(yCoord)-1][int(xCoord)-1] = noOfSide #shape
			fullGridInfo[2][int(yCoord)-1][int(xCoord)-1] = peri

			j = j+1
		i=i+1
    

	occupied_grids.sort(key = operator.itemgetter(0, 1))
'''
* Function name  :  makeGrid
* Inputs		 :	tuple, tuple
* Returns        : 	Grid of all objects and obstacles without the start point and end point
* Logic          :	checks if the current position is not the start or end point, appends to tmpGrid
* Example Call   :  makeGrid(source, destination)
'''
def makeGrid(source, destination):
	i = 0
	tmpGrid = []
	tSource = (source[0]+1, source[1]+1)
	tDestination = (destination[0]+1, destination[1]+1)
	while i < len(occupied_grids):
		if occupied_grids[i] != tSource and occupied_grids[i] != tDestination:
			tmpGrid.append((occupied_grids[i][0]-1, occupied_grids[i][1]-1))
		i = i + 1	

	return tmpGrid
'''
* Function name  :  createPath
* Inputs		 :	tuple, tuple
* Returns        : 	Dictionary of the path travelled, in the necessary format
* Logic          :	creates an object of Grid, and assigns the value of walls as the output of makeGrid
* Example Call   :  createPath(source, destination)
'''
def createPath(source, destination):
	graph = Grid(10, 10)
	graph.walls = makeGrid(source, destination)
	return (main_traverse(graph, source, destination))

'''
* Function name  :  removeObstacles
* Inputs		 :	None
* Returns        : 	None
* Logic          :	creates a list of tuples containing all details of th shapes in the grid
* Example Call   :  removeObstacles
'''
def removeObstacles():
	i = 0;j = 0
	while(i < len(occupied_grids)):
		x,y = occupied_grids[i]
		x = x-1; y = y-1
		if fullGridInfo[0][y][x] != 0 and fullGridInfo[0][y][x] != 4:
			objectList.append((int(fullGridInfo[0][y][x]), int(fullGridInfo[1][y][x]), int(fullGridInfo[2][y][x]), y, x))
		i += 1
	objectList.sort(key = operator.itemgetter(0, 1, 2, 3, 4))

'''
* Function name  :  match
* Inputs		 :	None
* Returns        : 	None
* Logic          :	matches the objects in the grid and calls createPath to find the path between them, appends the shortest path to planned_path
* Example Call   :  match()
'''
def match():
	i = 0; j = 0

	while (i < len(objectList)):
		j = 0
		flag = False
		tmpPath = {}
		minPath = {}
		minSteps = 100
		c = 0
		while (j < len(objectList)):
			if objectList[i][3] != objectList[j][3] or objectList[i][4] != objectList[j][4]:
				if objectList[i][0] == objectList[j][0] and objectList[i][1] == objectList[j][1] and abs(objectList[i][2]-objectList[j][2]) <= 2 :
					tmpPath = createPath((objectList[i][4], objectList[i][3]), (objectList[j][4], objectList[j][3]))

					if tmpPath[(objectList[i][4]+1, objectList[i][3]+1)][2] < minSteps:
						minSteps = tmpPath[(objectList[i][4]+1, objectList[i][3]+1)][2]
						minPath = tmpPath
						flag = True

			c = c+1
			j=j+1			

		if flag == False:
			minPath[(objectList[i][4]+1, objectList[i][3]+1)] = "NO MATCH", [], 0
			#print 'No Match'

		#print minPath
		
		planned_path.update(minPath)


		i = i+1



def main(image_filename):
	'''
This function is the main program which takes image of test_images as argument. 
Team is expected to insert their part of code as required to solve the given 
task (function calls etc).

***DO NOT EDIT THE FUNCTION NAME. Leave it as main****
Function name: main()

******DO NOT EDIT name of these argument*******
Input argument: image_filename

Return:
1 - List of tuples which is the coordinates for occupied grid. See Task2_Description for detail. 
2 - Dictionary with information of path. See Task2_Description for detail.
	'''

	



	##### WRITE YOUR CODE HERE - STARTS

	colorSeg(image_filename, 10)
	removeObstacles()
	match()
	#print occupied_grids
	#print planned_path

	# #### NO EDIT AFTER THIS

# DO NOT EDIT
# return Expected output, which is a list of tuples. See Task1_Description for detail.
	return occupied_grids, planned_path



'''
Below part of program will run when ever this file (task1_main.py) is run directly from terminal/Idle prompt.

'''
if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image4.jpg"

    main(image_filename)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
