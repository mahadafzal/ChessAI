import copy
import math
import random
from move import move

#define inputs
input1 = [['_', '_', '_', '_', '_', '_', 'q', 'k'],['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', '_', '_', 'P', '_', 'p'],['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', '_', '_', '_', 'Q', 'P'],['_', '_', '_', '_', '_', 'P', 'P', '_'],['_', '_', '_', '_', 'R', '_', 'K', '_']]
input2 = [['_', '_', 'B', '_', '_', '_', '_', '_'],['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', 'K', '_', '_', '_', '_'],['_', 'p', '_', '_', '_', '_', '_', '_'],['_', '_', 'k', '_', '_', '_', '_', '_'],['P', '_', '_', '_', '_', 'P', '_', '_'],['_', 'B', '_', '_', '_', '_', '_', '_'],['N', '_', '_', '_', '_', 'N', '_', '_']]
input3 = [['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', 'K', '_', '_', '_', '_'],['_', '_', 'R', '_', 'P', '_', '_', '_'],['_', 'P', '_', 'k', 'r', '_', '_', '_'],['_', '_', '_', 'N', 'p', 'b', '_', '_'],['_', '_', '_', '_', 'P', '_', '_', '_'],['_', '_', '_', '_', '_', '_', '_', '_'],['_', '_', '_', '_', '_', 'N', '_', '_']]

#variables for player and depth limit
white = "white"
black = "black"
depthLimit = 4

#function to display best state
def display(matrix):
	for row in matrix:
		for value in row:
			print(value, end = ' ')
		print("")

#Given a matrix and a player, returns the weighted value according to the number of pieces the current player has versus the pieces of the opponent
def evaluate(matrix, player):
	weight = 0
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):

			if(matrix[i][j] == 'P'):
				weight = weight + 1
				continue
			if(matrix[i][j] == 'p'):
				weight = weight - 1
				continue

			if(matrix[i][j] == 'N'):
				weight = weight + 3
				continue
			if(matrix[i][j] == 'n'):
				weight = weight - 3
				continue

			if(matrix[i][j] == 'B'):
				weight = weight + 3
				continue
			if(matrix[i][j] == 'b'):
				weight = weight - 3
				continue

			if(matrix[i][j] == 'R'):
				weight = weight + 5
				continue
			if(matrix[i][j] == 'r'):
				weight = weight - 5
				continue

			if(matrix[i][j] == 'Q'):
				weight = weight + 9
				continue
			if(matrix[i][j] == 'q'):
				weight = weight + 9
				continue

			if(matrix[i][j] == 'K'):
				weight = weight + 1000
			if(matrix[i][j] == 'k'):
				weight = weight - 1000

	return weight

#Policies that sort a given list of children for exploration

#Random exploration
def explorePolicy1(children):
		
		random.shuffle(children)
		return children

#Invasive exploration
def explorePolicy2(children, player):
	if (player == "white"):
		children.sort()
	elif (player == "black"):
		children.sort(reverse=True)

	return children

#Terminal test to see if the King has been captured of the opponent
def terminalTest(matrix, player):
	foundWhiteKing = True
	foundBlackKing = True
	if(move(matrix, player) == []):
		return True
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if(matrix[i][j] == 'K' and player == "black"):
				return False
			if(matrix[i][j] == 'k' and player == "white"):
				return False

	if(foundBlackKing == True and foundWhiteKing == True):
		return False

#Returns the best state that could be found given a player and a current state of the Board
def minimax(matrix, player, depth, alpha, beta, stats):
	
	#returns maximum value for alpha-beta pruning
	def maxi(matrix, alpha, beta, depth, stats):
		if(depth > depthLimit or terminalTest(matrix, white) == True):
			return evaluate(matrix, white)

		value = -99999
		successors = explorePolicy1(move(matrix, white))
		#successors = explorePolicy2(move(matrix, white), white)
		for child in successors:
			stats.setNodesChecked(stats.getNodesChecked() + 1)
			value = max(value, mini(child, alpha, beta, depth+1, stats))
			if (value >= beta):
				stats.setPruningOccurence(stats.getPruningOccurence() + 1)
				return value
			alpha = max(alpha, value)
		return value

	#returns minimum value for alpha-beta pruning
	def mini(matrix, alpha, beta, depth, stats):
		if(depth > depthLimit or terminalTest(matrix, black) == True):
			return evaluate(matrix, white)

		value = 99999
		successors = explorePolicy1(move(matrix, black))
		#successors = explorePolicy2(move(matrix, black), black)
		for child in successors:
			stats.setNodesChecked(stats.getNodesChecked() + 1)
			value = min(value, maxi(child, alpha, beta, depth+1, stats))
			if(value <= alpha):
				stats.setPruningOccurence(stats.getPruningOccurence() + 1)
				return value
			beta = min(beta, value)
		return value

	final_value = -99999
	beta = 99999
	best_move = []
	successors = explorePolicy1(move(matrix, white))
	#successors = explorePolicy2(move(matrix, white), white)
	for child in successors:
		stats.setNodesChecked(stats.getNodesChecked() + 1)
		value = mini(child, final_value, beta, 1, stats)

		if value > final_value:
			final_value = value
			best_move = child

	display(best_move)
	print("********")
	print("Value returned:", final_value)
	return best_move

#class to store statistics of results
class Stats(object):

	def __init__(self): 
		self.nodesChecked = 0
		self.pruningOccurence = 0

	def setNodesChecked(self, value):
		self.nodesChecked = value
	def getNodesChecked(self):
		return self.nodesChecked

	def setPruningOccurence(self, value):
		self.pruningOccurence = value
	def getPruningOccurence(self):
		return self.pruningOccurence

stats = Stats()
state = minimax(input1, white, depthLimit, -99999, 999999, stats)

print("Number of nodes checked:", stats.getNodesChecked())
print("Number of times pruning happens:", stats.getPruningOccurence())
