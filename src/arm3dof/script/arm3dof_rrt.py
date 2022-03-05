#!/usr/bin/env python3
#
#   rrt.py
#
import matplotlib.pyplot as plt
import numpy as np
import random

from fkin3 import fkin
from fkin5 import fkin5
from segInSphere import segInSphere



from sklearn.neighbors import KDTree
from prmtools import *

from planarutils import *
import line_to_line

######################################################################
#
#   General/World Definitions
#
#   List of objects, start, goal, and parameters.
#
amin, amax = -np.pi , np.pi

(startx, starty) = ( 1, 5)
(goalx,  goaly)  = (13, 5)

# Number of checks with intermediate states for ConnectsTo
MAX_CHECKS = 20;

dstep = 0.25
Nmax  = 1000

# arm link lengths
ls = np.array([0.0, 1.0, 1.0])
L  = ls.sum()

# radius of arm links
R = 0.1

# Construct the sphere (x, y, z, radius).
sphere1 = np.array([1.0, 0.0, 1.0, 0.6])
sphere2 = np.array([-1.0, 0.0, 1.0, 0.6])
sphere3 = np.array([0.0, 1.0, 1.0, 0.6])
sphere4 = np.array([0.0, -1.0, 1.0, 0.6])
obstacles = [sphere1, sphere2, sphere3, sphere4]

startts = np.array([0.0, 0.0, 0.0])
goalts  = np.array([0, np.pi / 2, 0])


######################################################################
#
#   State Definition
#
class State:
    def __init__(self, ts):
        # joints
        self.ts = ts
        self.cs = np.cos(ts) # precompute
        self.ss = np.sin(ts) # precompute

        # links
        self.ps = fkin(ls, ts, self.cs, self.ss)

        segments = []
        for i in range(len(self.ps)- 1):
            seg = np.hstack((self.ps[i],self.ps[i+1]))
            seg = np.hstack((seg, R)) # [1 x 7]
            segments.append(seg)
        self.segments = segments


    ############################################################
    # Utilities:
    # In case we want to print the state.
    def __repr__(self):
        repr_str = '< - '
        for i, t in enumerate(self.ts):
            repr_str += f'T{i} {t * (180/np.pi):5.1f} deg - '
        return repr_str + '>'


    # Return a tuple of the coordinates for KDTree.
    def Coordinates(self):
        return self.ps


    def InFreeSpace(self):
        return not (self.bodyCross() or self.obstacleCross())


    def bodyCross(self):
        for i in range(len(self.segments)):
            for j in range(i+2, len(self.segments)):
                if line_to_line.line_safe_distance(self.segments[i], self.segments[j]):
                    return True
        return False


    def obstacleCross(self):
        for i in range(len(self.segments)):
            for j in range(len(obstacles))  :
                if segInSphere(self.segments[i], obstacles[j]):
                    return True
        return False


    def Distance(self, other):
        return np.sqrt(np.power(np.abs(other.ts - self.ts), 2).sum())


    # Compute/create an intermediate state.
    def Intermediate(self, other, alpha):
        ts = self.ts + alpha * (other.ts - self.ts)
        return State(ts)


    # Check the local planner - whether this connects to another state.
    def ConnectsTo(self, other):
        n = len(self.ts);
        d = self.Distance(other)
        numConnects = int(np.ceil((MAX_CHECKS * d / (2 * np.pi * np.sqrt(n)))))

        for alpha in range(1, numConnects + 2):
            intermediate = self.Intermediate(other, alpha / numConnects)
            if not intermediate.InFreeSpace():
                return False
        return True

######################################################################
#
#   Tree Node Definition
#
#   Define a Node class upon which to build the tree.
#
class Node:
    def __init__(self, state, parentnode):
        # Save the state matching this node.
        self.state = state

        # Link to parent for the tree structure.
        self.parent = parentnode


######################################################################
#
#   RRT Functions
#
#   Again I am distiguishing state (containing x/y information) and
#   node (containing tree structure/parent information).
#
def RRT(tree, goalstate, Nmax):
    # Loop.
    while True:
        # Determine the target state.
        theta1 = random.uniform(amin, amax)
        theta2 = random.uniform(amin, amax)
        theta3 = random.uniform(amin, amax)
        targetstate = State(np.array([theta1, theta2, theta3]))        # How to pick x/y?

        # Find the nearest node (node with state nearest the target state).
        # This is inefficient (slow for large trees), but simple.
        list_vals = [(node.state.Distance(targetstate), node) for node in tree]
        (d2, nearnode)  = min(list_vals)
        d = np.sqrt(d2)
        nearstate = nearnode.state

        # Determine the next state, a step size (dstep) away.
        d_theta1 = targetstate.ts[0] - nearstate.ts[0]
        d_theta2 = targetstate.ts[1] - nearstate.ts[1]
        d_theta3 = targetstate.ts[2] - nearstate.ts[2]
        nextstate = State(np.array([nearstate.ts[0] + dstep * d_theta1,
                                    nearstate.ts[1] + dstep * d_theta2,
                                    nearstate.ts[2] + dstep * d_theta3]))

        # Check whether to attach (creating a new node).
        if nearstate.ConnectsTo(nextstate):
            nextnode = Node(nextstate, nearnode)
            tree.append(nextnode)

            # Also try to connect the goal.

            if  np.sqrt(nextstate.Distance(goalstate)) <= dstep:
                goalnode = Node(goalstate, nextnode)
                return(goalnode)

        # Check whether we should abort (tree has gotten too large).
        if (len(tree) >= Nmax):
            return None


def targetRRT(tree, goalstate, Nmax):
    # Loop.
    while True:
        # Determine the target state.
        if random.uniform(0,1) < 0.1:
            targetstate = goalstate
        else:
            theta1 = random.uniform(amin, amax)
            theta2 = random.uniform(amin, amax)
            theta3 = random.uniform(amin, amax)
            targetstate = State(np.array([theta1, theta2, theta3]))

        # Find the nearest node (node with state nearest the target state).
        # This is inefficient (slow for large trees), but simple.
        list_vals = [(node.state.Distance(targetstate), node) for node in tree]
        (d2, nearnode)  = min(list_vals)
        d = np.sqrt(d2)
        nearstate = nearnode.state

        # Determine the next state, a step size (dstep) away.
        d_theta1 = targetstate.ts[0] - nearstate.ts[0]
        d_theta2 = targetstate.ts[1] - nearstate.ts[1]
        d_theta3 = targetstate.ts[2] - nearstate.ts[2]
        nextstate = State(np.array([nearstate.ts[0] + dstep * d_theta1,
                                    nearstate.ts[1] + dstep * d_theta2,
                                    nearstate.ts[2] + dstep * d_theta3]))

        # Check whether to attach (creating a new node).
        if nearstate.ConnectsTo(nextstate):
            nextnode = Node(nextstate, nearnode)
            tree.append(nextnode)

            # Also try to connect the goal.

            if  np.sqrt(nextstate.Distance(goalstate)) <= dstep:
                goalnode = Node(goalstate, nextnode)
                return(goalnode)

        # Check whether we should abort (tree has gotten too large).
        if (len(tree) >= Nmax):
            return None

######################################################################
#
#  Main Code
#
def main():
    # Report the parameters.
    print('Running with step size ', dstep, ' and up to ', Nmax, ' nodes.')


    # Set up the start/goal states.
    startstate = State(startts)
    goalstate  = State(goalts)

    # Start the tree with the start state and no parent.
    tree = [Node(startstate, None)]

    # Execute the search (return the goal leaf node).
    node = targetRRT(tree, goalstate, Nmax)

    # Check the outcome
    if node is None:
        print("UNABLE TO FIND A PATH in %d steps", Nmax)
        input("(hit return to exit)")
        return

    # Show the path.
    paths = []
    while node.parent is not None:
        paths.append(node.parent.state)
        node = node.parent

    paths = paths[::-1]
    for val in paths:
        print(val)
    return paths

if __name__== "__main__":
    main()
