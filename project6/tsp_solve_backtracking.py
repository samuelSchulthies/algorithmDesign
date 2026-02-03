import copy
import math
import random
# from html.parser import incomplete

from utils import Tour, SolutionStats, Timer, score_tour, Solver
from cuttree import CutTree



def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []

    for i in range(len(edges)):
        if timer.time_out():
            break
        stat = greedy(edges, i, timer)
        if stat is not None:
            stats = addTour(stat, stats)

    return stats

def addTour(stat, stats):
    if len(stats) == 0:
        stats.append(stat)

    if stat.score < getLowestScore(stats).score:
        stats.append(stat)

    return stats

def getLowestScore(stats):
    lowestScoreTour = min(stats, key=lambda solution: solution.score)
    return lowestScoreTour

def greedy(edges, nodeIndex, timer):
    tour = [nodeIndex]
    for i in range(len(edges) - 1):

        nextNode, cost = getNextNode(edges, tour)

        if nextNode is None:
            return None
        else:
            tour.append(nextNode)

    if math.isinf(edges[tour[-1]][nodeIndex]):
        return None

    return SolutionStats(
        tour = copy.deepcopy(tour),
        score = score_tour(tour, edges),
        time = timer.time(),
        max_queue_size = 0,
        n_nodes_expanded = 0,
        n_nodes_pruned = 0,
        n_leaves_covered = 0,
        fraction_leaves_covered = 0
        )


def getNextNode(edges, tour):
    node = edges[tour[-1]]
    nodeCopy = [(cost, index) for index, cost in enumerate(node) if index not in tour]

    if len(nodeCopy) == 0:
        return None, 0

    cost, nextNode = min(nodeCopy)

    if math.isinf(cost):
        return None, cost

    return nextNode, cost


def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []



def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []

