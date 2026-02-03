progress = False

def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    return []


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    sortedByX = sorted(points, key=lambda tup: tup[0])
    return hull_recursor(sortedByX).getHull()


def hull_recursor(points):
    if len(points) == 1:
        point = Point(points[0])
        return Hull(point, point)
    else:
        leftHull = hull_recursor(points[:len(points) // 2])
        rightHull = hull_recursor(points[len(points) // 2:])

    return combine(leftHull, rightHull)

def combine(leftHull, rightHull):
    upperTangent = findTangents(leftHull.rightMostPoint, rightHull.leftMostPoint)
    lowerTangent = findTangents(rightHull.leftMostPoint, leftHull.rightMostPoint)

    upperTangent[1].setDirection(upperTangent[0])
    lowerTangent[1].setDirection(lowerTangent[0])

    combinedHull = Hull(leftHull.getLeft(), rightHull.getRight())

    hullList = [(combinedHull.getLeft().getX(), combinedHull.getLeft().getY())]
    combinedHull.listOfHullPoints = compileHullList(combinedHull.getLeft(), combinedHull.getLeft().getCounterClockwise(), hullList)

    return combinedHull


def compileHullList(initialPoint, point, hullList):

    if point != initialPoint:
        hullList.append((point.getX(), point.getY()))
        compileHullList(initialPoint, point.getCounterClockwise(), hullList)

    return hullList


def findTangents(leftHull: "Point", rightHull: "Point"):
    global progress
    progress = False

    leftHull = counterClockwise(leftHull, rightHull)
    rightHull = clockwise(leftHull, rightHull)
    if progress:
        return findTangents(leftHull, rightHull)
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
        return counterClockwise(leftHull.getCounterClockwise(), rightHull)
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
        return clockwise(leftHull, rightHull.clockwise)
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
