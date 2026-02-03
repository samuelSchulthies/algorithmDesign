# Project Report - Backtracking

## Baseline

### Design Experience

*I discussed with one of the TAs, Jacobus, about how greedy works. 
My implementation would consist of following the project spec in 
starting at a node, taking the least cost edge, and then storing a successful
tour if it was better than a previously found tour. My initial implementation ended up
being very messy and difficult to debug, so I reworked my execution with another TA, Isaac.*

### Theoretical Analysis - Greedy

### Time 
#### Our final time complexity will be O(n^3). In a successful run (where runtime is satisfactory), greedy assesses every node and every edge in every node. While exploring each edge we potentially take an additional cost of up to O(n) when checking which edges have been explored. Because of this, and that edges are equal to the amount of nodes, this run time is O(n^3)

```
def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:     O(n^3) - total run time
    stats = []

    for i in range(len(edges)):                                                     O(n^3) - this runs over every node, then every edge inside every node, then every edge again to check which is visted
        if timer.time_out():
            break
        stat = greedy(edges, i, timer)                                              O(n) - inherited worst case runtime
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

def greedy(edges, nodeIndex, timer):                    O(n - 1) - overall runtime
    tour = [nodeIndex]
    for i in range(len(edges) - 1):                     O(n - 1) - worst case is finding a successful tour and running over every edge minus 1. Number of edges in each node are equal to the number of nodes.

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


def getNextNode(edges, tour):                                                               O(n) - overall runtime
    node = edges[tour[-1]]
    nodeCopy = [(cost, index) for index, cost in enumerate(node) if index not in tour]      O(n) - worst case is this will run over every node toured

    if len(nodeCopy) == 0:
        return None, 0

    cost, nextNode = min(nodeCopy)

    if math.isinf(cost):
        return None, cost

    return nextNode, cost
```

### Space
#### The total space greedy will take is dependent on how many tours it finds. It can find, at most, one successful tour per start node. Thus if it finds one tour per node, we take up O(n) space in our return list

```
def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []

    for i in range(len(edges)):
        if timer.time_out():
            break
        stat = greedy(edges, i, timer)
        if stat is not None:
            stats = addTour(stat, stats)

    return stats                                                                    O(n) - worst case is we store a tour for every start node

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
    tour = [nodeIndex]                                  O(n) - this will store up to all the edges in the node
    for i in range(len(edges) - 1):                     

        nextNode, cost = getNextNode(edges, tour)

        if nextNode is None:
            return None
        else:
            tour.append(nextNode)

    if math.isinf(edges[tour[-1]][nodeIndex]):
        return None

    return SolutionStats(                               O(1) - intialization is constant
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
    nodeCopy = [(cost, index) for index, cost in enumerate(node) if index not in tour]      O(n) - worst case is we store every edge

    if len(nodeCopy) == 0:
        return None, 0

    cost, nextNode = min(nodeCopy)

    if math.isinf(cost):
        return None, cost

    return nextNode, cost
```

### Empirical Data - Greedy

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         | 0         |
| 10  | 0         | 0.0002    |
| 15  | 0         | 0.0004    |
| 20  | 0         | 0.0012    |
| 25  | 0         | 0.0023    |
| 30  | 0         | 0.0028    |
| 35  | 0         | 0.0080    |
| 40  | 0         | 0.0032    |
| 45  | 0         | 0.0041    |
| 50  | 0         | 0.0032    |


### Comparison of Theoretical and Empirical Results - Greedy

- Theoretical order of growth: O(n^2)
- Empirical order of growth (if different from theoretical): I ran my tsp algorithm with the same seed at each N in the table,
but the N values did not appear to be large enough to determine an empirical order of growth. The overall shape of the graph looks
to continue along an O(n^3) shape, but more data is needed to determine this.

![baselineGraph](images/baseline_plot.png)

## Core

### Design Experience

*Fill me in*

### Theoretical Analysis - Backtracking

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Backtracking

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         |           |
| 10  | 0         |           |
| 15  | 0         |           |
| 20  | 0         |           |
| 25  | 0         |           |
| 30  | 0         |           |
| 35  | 0         |           |
| 40  | 0         |           |
| 45  | 0         |           |
| 50  | 0         |           |

### Comparison of Theoretical and Empirical Results - Backtracking

- Theoretical order of growth: 
- Empirical order of growth (if different from theoretical):

### Greedy v Backtracking

*Fill me in*

### Water Bottle Scenario 

#### Scenario 1

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*


## Stretch 1

### Design Experience

*Fill me in*

### Demonstrate BSSF Backtracking Works Better than No-BSSF Backtracking 

*Fill me in*

### BSSF Backtracking v Backtracking Complexity Differences

*Fill me in*

### Time v Solution Cost

![Plot]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Cut Tree

*Fill me in*

### Plots 

*Fill me in*

## Project Review

*I reviewed my project with Jen Stone on November 22nd. We both implemented our code quite differently
but arrived at the same time and space complexity. I used multiple functions, Jen used one. Though the code was quite simple either way,
so I think both implementations were good. Our data structures were both similar, we used lists to track
edges visited. Our empirical data for baseline was very similar, and our graphs were quite similar too, so the constants
of proportionality would be very close.*

*Overall it was good reviewing with Jen, as I had missed part of my time complexity, mistaking my growth rate for O(n^2).
I had misunderstood that these reviews were only for if all tiers were finished. It was helpful comparing my code to Jen
and I will try to include reviews on my remaining projects.*
