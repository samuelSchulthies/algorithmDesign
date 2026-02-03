# Project Report - Convex Hull

## Baseline

### Design Discussion

*I discussed my design with Dion Kim. I explained to him I would implement
the divide and conquer algorithm recursively starting with the psuedo code from the homework.*

### Theoretical Analysis - Convex Hull Divide-and-Conquer

### Time 

#### Master Theorem Growth
*The master theorem states that:*

*a/b^d < 1, then O(n^d).*\
*a/b^d > 1, then O(n^log_b(a)).*\
*a/b^d = 1, then O((n^d)logn).*

With this in mind we will see where our code falls and if it matches the linear growth analyzed in the code below:

*a = how many sub problems?*\
*b = size of each sub problem*\
*d = recombine work after recursing*

*a = 2*\
*b = 2*\
*d = 1 (merge is linear, O(n^1))*

*Thus, 2/2^1 = 1, which in the master theorem correlates to O((n^d)logn), which simplifies to O(nlogn). 
Because n dominates logn, the master theorem theoretical growth closely matches a linear growth, 
even though the master theorem does not explicitly give a linear growth of O(n^d)*

#### Growth from Code Analysis
*Total run time: O(n). While unlikely, we may have all points already in a hull and have to walk over each in both halves, 
giving O(n). We must convert those points back to a list, which takes O(n).*

#### Conclusion on Growth
*Both the master theorem and the code point to a nearly linear growth of O(n)*


```
def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:      # O(n) - total worst cast
    sortedByX = sorted(points, key=lambda tup: tup[0])
    return hull_recursor(sortedByX).getHull()                                               # O(n) - inherited from function


def hull_recursor(points):                                                                  # O(n) - total worst case
    if len(points) == 1:
        point = Point(points[0])
        return Hull(point, point)
    else:
        leftHull = hull_recursor(points[:len(points) // 2])                             # O(logn) - constantly halving our amount as we recurse down
        rightHull = hull_recursor(points[len(points) // 2:])                            # O(logn) - constantly halving our amount as we recurse down

    return combine(leftHull, rightHull)                                                 # O(n) - total worst case of finding both tangents and converting points to list

def combine(leftHull, rightHull):
    upperTangent = findTangents(leftHull.rightMostPoint, rightHull.leftMostPoint)                                                       # O(n) - inherited from function
    lowerTangent = findTangents(rightHull.leftMostPoint, leftHull.rightMostPoint)                                                       # O(n) - inherited from function

    upperTangent[1].setDirection(upperTangent[0])
    lowerTangent[1].setDirection(lowerTangent[0])

    combinedHull = Hull(leftHull.getLeft(), rightHull.getRight())

    hullList = [(combinedHull.getLeft().getX(), combinedHull.getLeft().getY())]
    combinedHull.listOfHullPoints = compileHullList(combinedHull.getLeft(), combinedHull.getLeft().getCounterClockwise(), hullList)     # O(n) - inherited from function

    return combinedHull


def compileHullList(initialPoint, point, hullList):                                 # O(n) - total

    if point != initialPoint:
        hullList.append((point.getX(), point.getY()))
        compileHullList(initialPoint, point.getCounterClockwise(), hullList)        # O(n) - run through every node in the hull to convert back to points

    return hullList


def findTangents(leftHull: "Point", rightHull: "Point"):    # O(n) - total worst case
    global progress
    progress = False

    leftHull = counterClockwise(leftHull, rightHull)        # O(n/2) - inherited from function
    rightHull = clockwise(leftHull, rightHull)              # O(n/2) - inherited from function
    if progress:
        return findTangents(leftHull, rightHull)            # O(n) - recursion is dependent on the slope. Worst case is we check all nodes in both hulls, so n
    else:
        return leftHull, rightHull


def counterClockwise(leftHull: "Point", rightHull: "Point"):                                                                                    # O(n/2) - total
    global progress

    # Colinear check
    if (leftHull.getX() - rightHull.getX()) == 0 or (leftHull.getCounterClockwise().getX() - rightHull.getX()) == 0:
        return leftHull

    initialSlope = (leftHull.getY() - rightHull.getY()) / (leftHull.getX() - rightHull.getX())
    comparedSlope = (leftHull.getCounterClockwise().getY() - rightHull.getY()) / (leftHull.getCounterClockwise().getX() - rightHull.getX())

    if comparedSlope < initialSlope:
        progress = True
        return counterClockwise(leftHull.getCounterClockwise(), rightHull)                                                                      # O(n/2) - recursion is dependent on the slope. Worst case is we check all nodes in the left hull, so n/2
    else:
        return leftHull


def clockwise(leftHull: "Point", rightHull: "Point"):                                                                                           # O(n/2) - total
    global progress

    # Colinear check
    if (leftHull.getX() - rightHull.getX()) == 0 or (leftHull.getCounterClockwise().getX() - rightHull.getX()) == 0:
        return rightHull

    initialSlope = (leftHull.getY() - rightHull.getY()) / (leftHull.getX() - rightHull.getX())
    comparedSlope = (leftHull.getY() - rightHull.getClockwise().getY()) / (leftHull.getX() - rightHull.getClockwise().getX())

    if comparedSlope > initialSlope:
        progress = True
        return clockwise(leftHull, rightHull.clockwise)                                                                                         # O(n/2) - recursion is dependent on the slope. Worst case is we check all nodes in the right hull, so n/2
    else:
        return rightHull


class Hull:
    listOfHullPoints = []

    def __init__(self, leftPoint, rightPoint):
        self.leftMostPoint = leftPoint
        self.rightMostPoint = rightPoint

    def getLeft(self):
        return self.leftMostPoint

    def getRight(self):
        return self.rightMostPoint

    def setListOfHullPoints(self, leftList, rightList):
        self.listOfHullPoints = leftList + rightList

    def getHull(self):
        return self.listOfHullPoints

    def addHullPoint(self, point):
        self.listOfHullPoints.append(point)


class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.counterClockwise = self
        self.clockwise = self

    def setDirection(self, point):
        self.counterClockwise = point
        point.clockwise = self

    def getClockwise(self):
        return self.clockwise

    def getCounterClockwise(self):
        return self.counterClockwise

    def getX(self):
        return self.x

    def getY(self):
        return self.y
```

### Space

#### *Final space would be O(n). The most memory we use at any point is within the recursion call stack, which is cleared once the recursion finishes*
```
def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]: 
    sortedByX = sorted(points, key=lambda tup: tup[0])
    return hull_recursor(sortedByX).getHull()                                               # O(1) - inherited from function


def hull_recursor(points):                                                              
    if len(points) == 1:
        point = Point(points[0])
        return Hull(point, point)
    else:
        leftHull = hull_recursor(points[:len(points) // 2])                             # O(logn) - constantly halving our amount as we recurse down
        rightHull = hull_recursor(points[len(points) // 2:])                            # O(logn) - constantly halving our amount as we recurse down

    return combine(leftHull, rightHull)                                                 # O(1) - inherited from function                           

def combine(leftHull, rightHull):                                                                                                      
    upperTangent = findTangents(leftHull.rightMostPoint, rightHull.leftMostPoint)                                                      
    lowerTangent = findTangents(rightHull.leftMostPoint, leftHull.rightMostPoint)                                                 

    upperTangent[1].setDirection(upperTangent[0])
    lowerTangent[1].setDirection(lowerTangent[0])

    combinedHull = Hull(leftHull.getLeft(), rightHull.getRight())                                                                       # O(1) - we only have 1 hull after combining

    hullList = [(combinedHull.getLeft().getX(), combinedHull.getLeft().getY())]
    combinedHull.listOfHullPoints = compileHullList(combinedHull.getLeft(), combinedHull.getLeft().getCounterClockwise(), hullList)     # O(n) - inherited from function

    return combinedHull


def compileHullList(initialPoint, point, hullList):                                 

    if point != initialPoint:
        hullList.append((point.getX(), point.getY()))
        compileHullList(initialPoint, point.getCounterClockwise(), hullList)        # O(n) - worst case store all points 

    return hullList


def findTangents(leftHull: "Point", rightHull: "Point"):  
    global progress
    progress = False

    leftHull = counterClockwise(leftHull, rightHull)        # O(n/2) - inherited from function
    rightHull = clockwise(leftHull, rightHull)              # O(n/2) - inherited from function
    if progress:
        return findTangents(leftHull, rightHull)            # O(n) - worst case checking every node, so we recurse n times 
    else:
        return leftHull, rightHull


def counterClockwise(leftHull: "Point", rightHull: "Point"):                                                                             
    global progress

    # Colinear check
    if (leftHull.getX() - rightHull.getX()) == 0 or (leftHull.getCounterClockwise().getX() - rightHull.getX()) == 0:
        return leftHull

    initialSlope = (leftHull.getY() - rightHull.getY()) / (leftHull.getX() - rightHull.getX())
    comparedSlope = (leftHull.getCounterClockwise().getY() - rightHull.getY()) / (leftHull.getCounterClockwise().getX() - rightHull.getX())

    if comparedSlope < initialSlope:
        progress = True
        return counterClockwise(leftHull.getCounterClockwise(), rightHull)                                                                      # O(n/2) - Worst case is we check all nodes in the left hull, so rescursive stack will be half of our points
    else:
        return leftHull


def clockwise(leftHull: "Point", rightHull: "Point"):                                                                                         
    global progress

    # Colinear check
    if (leftHull.getX() - rightHull.getX()) == 0 or (leftHull.getCounterClockwise().getX() - rightHull.getX()) == 0:
        return rightHull

    initialSlope = (leftHull.getY() - rightHull.getY()) / (leftHull.getX() - rightHull.getX())
    comparedSlope = (leftHull.getY() - rightHull.getClockwise().getY()) / (leftHull.getX() - rightHull.getClockwise().getX())

    if comparedSlope > initialSlope:
        progress = True
        return clockwise(leftHull, rightHull.clockwise)                                                                                         # O(n/2) - Worst case is we check all nodes in the right hull, so rescursive stack will be half of our points
    else:
        return rightHull


class Hull:                                                 # O(1) - at any give time we have at most 2 hulls which quickly combine to one, thus this takes up constant space 
    listOfHullPoints = []

    def __init__(self, leftPoint, rightPoint):
        self.leftMostPoint = leftPoint
        self.rightMostPoint = rightPoint

    def getLeft(self):
        return self.leftMostPoint

    def getRight(self):
        return self.rightMostPoint

    def setListOfHullPoints(self, leftList, rightList):
        self.listOfHullPoints = leftList + rightList

    def getHull(self):
        return self.listOfHullPoints

    def addHullPoint(self, point):
        self.listOfHullPoints.append(point)


class Point:                                  # O(n) - worst case is we have to store every point given
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.counterClockwise = self
        self.clockwise = self

    def setDirection(self, point):
        self.counterClockwise = point
        point.clockwise = self

    def getClockwise(self):
        return self.clockwise

    def getCounterClockwise(self):
        return self.counterClockwise

    def getX(self):
        return self.x

    def getY(self):
        return self.y
```

## Core

### Design Discussion

*I discussed my one failed test case with Dion Kim, which was test_multiple_adjusts_dvcq. This was an easy fix,
I just needed to add in checking for colinear lines.*  

### Empirical Data - Convex Hull Divide-and-Conquer

| N     | time (ms) |
|-------|-----------|
| 10    | .0003     |
| 100   | .0027     |
| 1000  | .0253     |
| 10000 | .2620     |
| 20000 | .5098     |
| 40000 | 1.0578    |
| 50000 | 1.3178    |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: *O(n)* 
- Empirical order of growth (if different from theoretical): *Same as above*

![empirical](plots/plot_core_linear.png)

#### *My theoretical analysis was correct. I had predicted a worst case of O(n), which would be due to running over every point in the convex hull.*

## Stretch 1

### Design Discussion

*Fill me in*

### Chosen Convex Hull Implementation Description

*Fill me in*

### Empirical Data

| N     | time (ms) |
|-------|-----------|
| 10    |           |
| 100   |           |
| 1000  |           |
| 10000 |           |
| 20000 |           |
| 40000 |           |
| 50000 |           |

### Comparison of Chosen Algorithm with Divide-and-Conquer Convex Hull

#### Algorithmic Differences

*Fill me in*

#### Performance Differences

*Fill me in*

## Stretch 2

*Fill me in*

## Project Review

*Fill me in*

