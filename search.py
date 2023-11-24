# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import PriorityQueue
from util import Queue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getTotalNodes(self):
        """
        Returns the total number of nodes in the search space. This method needs
        to be implemented by subclasses based on the specific problem context.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    frontier = Stack()
    reached = []
    solution = []
    cost = 0

    frontier.push((problem.getStartState(), solution, cost))

    while not frontier.isEmpty():
        current_node = frontier.pop()
        position = current_node[0]
        solution = current_node[1]

        if position not in reached:
            reached.append(position)

        if problem.isGoalState(position):
            return solution

        for item in problem.getSuccessors(position):
            if item[0] not in reached:
                frontier.push((item[0], solution + [item[1]], item[2]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    frontier = Queue()
    reached = []
    solution = []
    cost = 0

    frontier.push((problem.getStartState(), solution, cost))

    while not frontier.isEmpty():

        # First node in frontier
        current_node = frontier.pop()
        position = current_node[0]
        solution = current_node[1]

        if position not in reached:
            reached.append(position)

        if problem.isGoalState(position):
            return solution

        # Pushes the current node's successors to the Queue if they are not reached.
        # We check both reached and frontier.
        for item in problem.getSuccessors(position):
            if item[0] not in reached and item[0] not in (node[0] for node in frontier.list):
                frontier.push((item[0], solution + [item[1]], item[2]))

    util.raiseNotDefined()


def uniformCostSearch(problem):
    frontier = PriorityQueue()
    reached = []
    solution = []

    frontier.push((problem.getStartState(), solution), 0)

    while not frontier.isEmpty():
        current_node = frontier.pop()
        position = current_node[0]
        solution = current_node[1]

        if position not in reached:
            reached.append(position)

        if problem.isGoalState(position):
            return solution

        for successor, action, cost in problem.getSuccessors(position):

            new_path = solution + [action]
            new_cost = problem.getCostOfActions(new_path)

            # Find the best known cost for the successor, if it exists
            existing_cost = next((c for n, c in reached if n == successor), None)

            if successor not in reached:
                if existing_cost is None or existing_cost > new_cost:
                    frontier.push((successor, new_path), new_cost)
                    # Update or add the cost for the successor
                    if existing_cost is not None:
                        reached = [(n, c) if n != successor else (successor, new_cost) for n, c in reached]
                    else:
                        reached.append((successor, new_cost))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    frontier = PriorityQueue()
    reached = []
    solution = []
    priority = 0  # Initializes the priority to 0.

    # Pushes the start position to the PriorityQueue.
    frontier.push((problem.getStartState(), solution), priority)

    while not frontier.isEmpty():

        current_node = frontier.pop()
        position = current_node[0]
        solution = current_node[1]

        # Returns the final path if the current position is goal.
        if problem.isGoalState(position):
            return solution

        # Pushes the current position to the reached list if it is not reached.
        if position not in reached:
            reached.append(position)

            # Gets successors of the current node.
            successors = problem.getSuccessors(position)

            # Pushes the current node's successors to the PriorityQueue if they are not reached.
            for item in successors:
                if item[0] not in reached:
                    # new position
                    npo = item[0]
                    # new path
                    npa = solution + [item[1]]

                    # Updates priority of the successor using f(n) function.

                    """ g(n): Current cost from start state to the current position. """
                    g = problem.getCostOfActions(npa)

                    """ h(n): Estimate of the lowest cost from the current position to the goal state. """
                    h = heuristic(npo, problem)

                    """ f(n): Estimate of the lowest cost of the solution path
                              from start state to the goal state passing through the current position """
                    frontier.push((npo, npa), g + h)

    util.raiseNotDefined()


#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE ***"
    limit = 0

    while True:  # Keep increasing the depth limit until a solution is found
        frontier = Stack()
        reached = []  # Track visited states at each depth level
        solution = []

        frontier.push((problem.getStartState(), solution, 0))  # (state, path to state, depth)

        while not frontier.isEmpty():

            current_node = frontier.pop()
            position = current_node[0]
            solution = current_node[1]
            cost = current_node[2]

            # Check for revisiting in the current depth iteration
            if position not in reached:
                reached.append(position)

                if problem.isGoalState(position):
                    return solution  # Return path to goal state

                # Add successors if within the depth limit
                if cost < limit:
                    for son in problem.getSuccessors(position):
                        if cost + son[2] <= limit:
                            frontier.push((son[0], solution + [son[1]], cost + son[2]))

        limit += 1


    

#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
