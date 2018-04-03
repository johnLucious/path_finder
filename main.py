# IF2210: Algorithm Strategies #

import os
import math
import os.path

listNode = []		
listOfNodes = []

class ofNode:
	def __init__(self):
		self.cost = 0
		self.visitedNode = []
		self.name = ""
		
	def setName(self, name):
		self.name = name
	
	def addCost(self, costAdd):
		self.cost += costAdd
		
	def getName(self):
		return self.name
	
	def getCost(self):
		return self.cost

class Node:
	def __init__(self):
		self.nodeAdj = []

	def getAdjNode(self, i):
		return self.nodeAdj[i]
	
	def addAdjNode(self, point):
		self.nodeAdj.append(point)

	def showAdjNodes(self):
		return self.nodeAdj
		
	

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False		

def createFile():
	s = input("File name: ")
	s = s + ".txt"
	file = open(s, "w")
	
	reqAcc = False
	while not reqAcc:
		try:
			print("Input Number of Nodes")
			nNodes = int(input('> '))
			if (nNodes < 3):
				raise
		except:
			print("::ReqError: Minimum input must be 8")
			print()
		else:
			print("::Making required size of nodes")
			print()
			reqAcc = True

	print("Input name of each nodes:")
	point = ""
	for i in range(nNodes-1):
		s = input(str(i+1) + "> ").split()
		nodeName = s[0].lower()
		point = point + s[1].lower() + "," + s[2].lower() + " "
		file.write(nodeName + " ")
	s = input(str(i+2) + "> ").split()
	nodeName = s[0].lower()
	point = point + s[1].lower() + "," + s[2].lower() + "\n"
	file.write(nodeName + "\n")
	file.write(point)

	print("Input set number of integer")
	for i in range(nNodes):
		validInput = True
		setOfNum = input(str(i+1) + "> ")
		fileString = setOfNum
		setOfNum = setOfNum.split()
		for j in range(len(setOfNum)):
			if (not isNumber(setOfNum[j])):
				validInput = False
		while (len(setOfNum) != nNodes or not validInput):
			validInput = True
			print("::ReqError: Element of number must be " + str(nNodes) + " and must be number")
			print()
			setOfNum = input(str(i+1) + "> ")
			fileString = setOfNum
			setOfNum = setOfNum.split()
			
			for j in range(len(setOfNum)):
				if (not isNumber(setOfNum[j])):
					validInput = False
		
		file.write(fileString + "\n")
	file.close()

def readFile():
	matrix = []
	path = input("File name: ")
	path += ".txt"
	if os.path.isfile(path) and os.access(path, os.R_OK):
		firstLine = True
		secondLine = False
		with open(path, "r") as file:
			for line in file:
				vector = []
				if (firstLine):
					line = line.split()
					for i in range(len(line)):
						vector.append(line[i])
					firstLine = False
					secondLine = True
				elif (secondLine):
					line = line.split()
					print(line)
					for i in range(len(line)):
						temp = line[i].split(",")
						point = tuple((float(temp[0]), float(temp[1])))
						vector.append(point)
					secondLine = False
				else:
					line = line.split()
					for i in range(len(line)):
						vector.append(float(line[i]))
				matrix.append(vector)
		print("File added to memory")
		return matrix
	else:
		print("::FileError: Either file is missing or is not readable")
		return None

def returnNode(node, matrix):
	for i in range(len(matrix[0])):
		if (matrix[0][i] == node):
			n = i
			break
	return n
	
def euclidDist(pointA, pointB):
	x = pointA[0] - pointB[0]
	y = pointA[1] - pointB[1]
	return math.sqrt(pow(x,2) + pow(y,2))

def determineCost(nodeA, nodeB, matrix):
	pathCost = matrix[returnNode(nodeA, matrix) + 2][returnNode(nodeB, matrix)]
	heuristicCost = euclidDist(matrix[1][returnNode(nodeA, matrix)], matrix[1][returnNode(nodeB, matrix)])

	return (pathCost + heuristicCost)

def findLowestCost():
	cost = 99999999
	chosenNode = None
	for node in listOfNodes:
		if (cost > node.getCost()):
			cost = node.getCost()
			chosenNode = node.getName()
	return chosenNode
	
def findPath(start, final, matrix):
	global listNode, listOfNodes
	currentNode = start
	resultNode = [start]
	
	while not (currentNode == final):
		for i in range(len(listNode[returnNode(currentNode, matrix)].showAdjNodes())):
			print("flag")
			node = ofNode()
			node.setName(listNode[returnNode(currentNode, matrix)].getAdjNode(i))
			node.addCost(determineCost(currentNode, matrix[0][listNode[returnNode(currentNode, matrix)].getAdjNode(i)], matrix))
			print(node.getCost())
			listOfNodes.append(node)
			print(listOfNodes)
		currentNode = findLowestCost()
		resultNode.append(currentNode)
		
	return resultNode
		
def findAdj(matrix):
	global listNode
	
	for i in range(len(matrix[0])):
		nodes = Node()
		for j in range(len(matrix[i+2])):
			if (matrix[i+2][j] != -1):
				nodes.addAdjNode(j)
		listNode.append(nodes)

def containAt(s, vector):
	contain = False
	for i in range(len(vector)):
		if (s == vector[i]):
			contain = True
	return contain

def main():
	global listNode
	
	matrix = None
	s = input("Command> ")
	while (s != "exit"):
		if (s == "new"):
			createFile()
		elif (s == "read"):
			matrix = readFile()
		elif (s == "find"):
			if (matrix == None):
				print("::FileError: Data not found")
			else:
				findAdj(matrix)
				print("List of Nodes:")
				for i in range(len(matrix[0])):
					print(matrix[0][i], end = " ")
				print("\n")
				print("Input Start and Final State:")
				s = input("> ").split()
				if (len(s) == 2):
					if ((containAt(s[0], matrix[0])) and (containAt(s[1], matrix[0]))):
						start = s[0]
						final = s[1]
						findPath(start, final, matrix)
					else:
						print("::StatError: State(s) not found")
				elif (len(s) < 2):
					print("::ArgError: Missing arguments, arguments must be 2")
				else:
					print("::ArgError: Arguments must be 2, but found " + str(len(s)) + " arguments")
		else:
			print("::CommError: Command not found")
		print()
		s = input("Command> ")

main()