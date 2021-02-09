# A* Search Executable Game
Small project made to create an executable file that, using pygame, can display a visualisation of A* search at work (used by Google Maps)


# A* Search  Algorithm
A* is an informed search algorithm (algorithm knows the location of the end node when starting) that is always guaranteed to find the shortest path between a start and end node.

It does so by making use of a heuristic function (a_star_heuristic) to determine which search path to extend. This is based on the current cost of the path plus the expected cost of the rest of the path (guessed by heuristic) which is formulated as: f(n) = g(n) + h(n)

- g(n): the cost of the current path from start to the current node
- h(n): the result of the heuristic function used to guess the expected cost/path length from the next node to the end node
- f(n): the addition of these two, the value of which is used to direct the search

Primary characteristics:

| +/-        | Characteristic           | Explanation  |
| ------------- |:-------------:| :-----:|
| +      |  Complete | If the solution exist, it is guaranteed to be found |
| +     | Optimal |   Guaranteed to find the shortest path |
| - | Complex - O(b^d^) |    Stores all observed nodes in memory |


