import numpy as np

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap_open_penalty=0,
        gap='-',
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap_open_penalty: how much it costs to open a gap. If 0, there is no gap_open penalty
        :param gap: the character to use to represent gaps in the alignment strings
    """
    alignmentTemplate = buildTemplate(seq1, seq2)
    alignmentDictionary = buildDictionary(alignmentTemplate)
    computedCosts = calculateCosts(alignmentTemplate, alignmentDictionary, indel_penalty, match_award, sub_penalty)
    finalCost = computedCosts[len(alignmentTemplate) - 1, len(alignmentTemplate[0]) - 1].getCost()
    alignedSequence = buildStrings(alignmentTemplate, alignmentDictionary)

    return finalCost, alignedSequence[0], alignedSequence[1]


def buildTemplate(seq1, seq2):
    emptySquares = 2

    alignmentTemplate = [[0] * (len(seq2) + emptySquares) for _ in range(len(seq1) + emptySquares)]
    alignmentTemplate[0][2:] = list(seq2)

    iterator = 0
    for i in range(2, len(seq1) + emptySquares):
        alignmentTemplate[i][0] = seq1[iterator]
        iterator += 1

    return alignmentTemplate


def buildDictionary(alignmentTemplate):
    alignmentDictionary = {}
    for row in range(len(alignmentTemplate)):
        for col in range(len(alignmentTemplate[0])):
            alignmentDictionary[(row, col)] = CellData(0, "", alignmentTemplate[row][col], False)

    return alignmentDictionary


def calculateCosts(alignmentTemplate, alignmentDictionary, indel_penalty, match_award, sub_penalty):
    for row in range(1, len(alignmentTemplate)):
        for col in range(1, len(alignmentTemplate[0])):
            match = False
            currentCell = (row, col)
            topCellCost = alignmentDictionary[(row - 1, col)].getCost() + indel_penalty
            leftCellCost = alignmentDictionary[(row, col - 1)].getCost() + indel_penalty

            if alignmentDictionary[(0, col)].getName() == alignmentDictionary[(row, 0)].getName() and row != 1 and col != 1:
                diagonalCellCost = alignmentDictionary[(row - 1, col - 1)].getCost() + match_award
                match = True
            else:
                diagonalCellCost = alignmentDictionary[(row - 1, col - 1)].getCost() + sub_penalty


            if row == 1 and col != 1:
                alignmentDictionary[currentCell] = CellData(leftCellCost, "left", "-", False)
                alignmentTemplate[currentCell[0]][currentCell[1]] = leftCellCost

            if col == 1 and row != 1:
                alignmentDictionary[currentCell] = CellData(topCellCost, "up", "-", False)
                alignmentTemplate[currentCell[0]][currentCell[1]] = topCellCost

            elif row != 1 and col != 1:
                lowestCost = sortCosts([(topCellCost, "up"), (leftCellCost, "left"), (diagonalCellCost, "diagonal")])
                alignmentDictionary[currentCell] = CellData(lowestCost[0], lowestCost[1], "-", match)
                alignmentTemplate[currentCell[0]][currentCell[1]] = lowestCost[0]

    return alignmentDictionary


def buildStrings(alignmentTemplate, alignmentDictionary):
    path = []
    alignedSequence1 = ""
    alignedSequence2 = ""
    rowCol = (len(alignmentTemplate) - 1, len(alignmentTemplate[0]) - 1)
    path = buildLoop(path, alignmentDictionary, rowCol)
    path.reverse()

    for cellDataSet in path:
        if cellDataSet[0] == "diagonal":
            alignedSequence1 += alignmentDictionary[cellDataSet[2][0], 0].getName()
            alignedSequence2 += alignmentDictionary[0, cellDataSet[2][1]].getName()

        elif cellDataSet[0] == "up":
            alignedSequence1 += alignmentDictionary[cellDataSet[2][0], 0].getName()
            alignedSequence2 += "-"

        elif cellDataSet[0] == "left":
            alignedSequence1 += "-"
            alignedSequence2 += alignmentDictionary[0, cellDataSet[2][1]].getName()

    return alignedSequence1, alignedSequence2

def buildLoop(path, alignmentDictionary, rowCol):
    row = rowCol[0]
    col = rowCol[1]

    while row and col != 0:
        currentCell = alignmentDictionary[(row, col)]
        path.append((currentCell.getDirection(), currentCell.isMatch, (row, col)))

        if currentCell.getDirection() == "up":
            row -= 1
        elif currentCell.getDirection() == "left":
            col -= 1
        elif currentCell.getDirection() == "diagonal":
            row -= 1
            col -= 1
        else:
            row = 0
            col = 0

    return path


def sortCosts(costs):
    lowestCost = min(costs, key=lambda tup: (tup[0], tup[1]))
    return lowestCost


class CellData:
    def __init__(self, cost, direction, name, isMatch):
        self.cost = cost
        self.direction = direction
        self.name = name
        self.isMatch = isMatch

    def getCost(self):
        return self.cost

    def getDirection(self):
        return self.direction

    def getName(self):
        return self.name

    def getIsMatch(self):
        return self.isMatch

