#!/usr/bin/env python3
#
#   arm3dof.py
#
import bisect
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from sklearn.neighbors import KDTree


######################################################################
#
#   World
#   List of objects, start, goal, and parameters.
#
ls = np.array([0.0, 1.0, 1.0]) # arm link lengths
L  = ls.sum()


# Construct the walls (boxes) (x, y, z, roll, pitch, yaw, length, width, height).
floor      = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2*L, 2*L, 0.0])
ceiling    = np.array([0.0, 0.0, L, 0.0, 0.0, 0.0, 2*L, 2*L, 0.0])
x_pos_wall = np.array([L, 0.0, L/2, 0.0, 0.0, 0.0, 0.0, 2*L, L])
x_neg_wall = np.array([-L, 0.0, L/2, 0.0, 0.0, 0.0, 0.0, 2*L, L])
y_pos_wall = np.array([0, L, L/2, 0.0, 0.0, 0.0, 2*L, 0.0, L])
y_neg_wall = np.array([0, -L, L/2, 0.0, 0.0, 0.0, 2*L, 0.0, L])

obstacles = [floor, ceiling,
             x_pos_wall, x_neg_wall,
             y_pos_wall, y_neg_wall]


# Pick your start and goal locations (in radians).
startts = np.array([0.0, 0.0, 0.0])
goalts  = np.array([1.16, 2.36, -1.49])


# PRM default parameters
N = 800
K = 50


# RRT default parameters
dstep = 0.25
Nmax  = 1000


######################################################################
#
#   State Definition
#
class State:
    def __init__(self, ts):
        # Pre-compute the trigonometry.
        self.ts = ts
        self.cs = np.cos(ts)
        self.ss = np.sin(ts)
        self.ps = fkin(ts, cs, ss)


    ############################################################
    # Utilities:
    # In case we want to print the state.
    def __repr__(self):
        repr_str = '< - '
        for i, t in enumerate(self.ts):
            repr_str += f'T{i} {t * (180/np.pi):5.1f} deg - '
        return repr_str + '>'

    # Draw where the state is:
    #def Draw(self, *args, **kwargs):
    #    plt.plot(self.x, self.y, *args, **kwargs)
    #    plt.pause(0.001)


    ############################################################
    # PRM Functions:
    # Check whether in free space.
    #def InFreeSpace(self):
    #    for wall in walls:
    #        if SegmentCrossBox(wall, self.box):
    #            return False
    #    return True

    # Compute the relative distance to another state.  Scale the
    # angular error by the car length.
    #def Distance(self, other):
    #    return np.sqrt((self.x - other.x)**2 +
    #                   (self.y - other.y)**2 +
    #                   (wheelbase*AngleDiff(self.t, other.t))**2)


    ############################################################
    # RRT Functions:
    # Compute the relative distance to another state.
    #def DistSquared(self, other):
    #    return ((self.x - other.x)**2 + (self.y - other.y)**2)

    # Compute/create an intermediate state.
    #def Intermediate(self, other, alpha):
    #    return State(self.x + alpha * (other.x - self.x),
    #                 self.y + alpha * (other.y - self.y))

    # Check the local planner - whether this connects to another state.
    #def ConnectsTo(self, other):
    #    for triangle in triangles:
    #        if SegmentCrossTriangle(((self.x, self.y), (other.x, other.y)),
    #                                triangle):
    #            return False
    #    return True


def main():
    # Report the parameters.
    print('Running with ', N, ' nodes and ', K, ' neighbors.')


    # Create the start/goal nodes.
    #startnode = Node(State(startts))
    #goalNode  = Node(State(goalts))
    print(State(startts))
    print(State(goalts))

    # Show the start/goal states.
    #startnode.state.Draw(fig, 'r', linewidth=2)
    #goalnode.state.Draw(fig,  'r', linewidth=2)
    #fig.ShowFigure()
    #input("Showing basic world (hit return to continue)")


    # Create the list of sample points.
    #start = time.time()
    nodeList = []
    #AddNodesToListObj(nodeList, N)
    #print('Sampling took ', time.time() - start)

    # # Show the sample states.
    #for node in nodeList:
    #    node.state.Draw(fig, 'k', linewidth=1)
    #fig.ShowFigure()
    #input("Showing the nodes (hit return to continue)")

    # Add the start/goal nodes.
    #nodeList.append(startnode)
    #nodeList.append(goalnode)


    # Connect to the nearest neighbors.
    #start = time.time()
    #ConnectNearestNeighbors(nodeList, K)
    #print('Connecting took ', time.time() - start)

    # # Show the neighbor connections.
    # for node in nodeList:
    #     for child in node.children:
    #         plan = LocalPlan(node.state, child.state)
    #         plan.Draw(fig, 'g-', linewidth=0.5)
    # fig.ShowFigure()
    # input("Showing the full graph (hit return to continue)")


    # Run the A* planner.
    #start = time.time()
    #path = AStar(nodeList, startnode, goalnode)
    #print('A* took ', time.time() - start)
    #if not path:
    #    print("UNABLE TO FIND A PATH")
    #    return


    # Show the path.
    #DrawPath(path, fig, 'r', linewidth=1)
    #fig.ShowFigure()
    #input("Showing the raw path (hit return to continue)")

    # Post Process the path.
    #path = PostProcess(path)

    # Show the post-processed path.
    #DrawPath(path, fig, 'b', linewidth=2)
    #fig.ShowFigure()
    #input("Showing the post-processed path (hit return to continue)")


if __name__== "__main__":
    main()