"""Generic search algorithms for the Panini logistics workshop."""

from __future__ import annotations

from typing import Any

from algorithms import utils
from algorithms.heuristics import nullHeuristic
from algorithms.problems import SearchProblem, State


def _remember_frontier(problem: SearchProblem, frontier: Any) -> None:
    """Record the largest frontier size reached during a search.

    Call this helper after each push/pop cycle in DFS, BFS, UCS and A*.
    It updates `problem._max_frontier_size`, which `main.py` prints in the
    execution summary for your experimental analysis.

    You do not need to count expanded nodes here: `getSuccessors` in
    `algorithms/problems.py` already increments `problem._expanded`.
    """

    if hasattr(frontier, "_items"):
        size = len(frontier._items)
    elif hasattr(frontier, "heap"):
        size = len(frontier.heap)
    else:
        size = 0
    current = getattr(problem, "_max_frontier_size", 0)
    problem._max_frontier_size = max(current, size)


def depthFirstSearch(problem: SearchProblem) -> list[str]:
    """Search the deepest nodes in the search tree first.

    Tips:
    - Return the action list accumulated along the path, not the node sequence.
    - Call `_remember_frontier` whenever the frontier changes.
    - Expanded nodes are counted automatically inside `getSuccessors`.
    """

    frontier = utils.Stack()
    start = problem.getStartState()
    frontier.push((start, []))
    visited = set()
    
    while not frontier.isEmpty():
        _remember_frontier(problem, frontier)
        node, actions = frontier.pop()
        
        if node in visited:
            continue
        visited.add(node)
        
        if problem.isGoalState(node):
            return actions
        
        for next_node, action, cost in problem.getSuccessors(node):
            if next_node not in visited:
                frontier.push((next_node, actions + [action]))
    
    return []


def breadthFirstSearch(problem: SearchProblem) -> list[str]:
    """Search the shallowest nodes in the search tree first.

    Tips:
    - Mark a state as visited when you enqueue it, not when you dequeue it.
    - Test for the goal immediately after dequeuing a state.
    """

    frontier = utils.Queue()
    start = problem.getStartState()
    frontier.push((start, []))
    visited = {start}
    
    while not frontier.isEmpty():
        _remember_frontier(problem, frontier)
        node, actions = frontier.pop()
        
        if problem.isGoalState(node):
            return actions
        
        for next_node, action, cost in problem.getSuccessors(node):
            if next_node not in visited:
                visited.add(next_node)
                frontier.push((next_node, actions + [action]))
    
    return []


def uniformCostSearch(problem: SearchProblem) -> list[str]:
    """Search the node with the lowest path cost first.

    Tips:
    - Use path cost `g(n)` as the priority queue key.
    - Ignore stale frontier entries whose stored `g` is worse than the best known.
    """

    frontier = utils.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0.0), 0.0)  # (node, actions, cost), priority=cost
    visited = {}  # node -> best_cost_seen
    
    while not frontier.isEmpty():
        _remember_frontier(problem, frontier)
        node, actions, cost = frontier.pop()
        
        # Si ya visitamos este nodo con mejor costo, ignorar
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost
        
        if problem.isGoalState(node):
            return actions
        
        for next_node, action, edge_cost in problem.getSuccessors(node):
            new_cost = cost + edge_cost
            if next_node not in visited or visited[next_node] > new_cost:
                frontier.push((next_node, actions + [action], new_cost), new_cost)
    
    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> list[str]:
    """Search the node with the lowest `g(n) + h(n)` first.

    Tips:
    - Push `g(n) + h(n)` to the frontier, but compare re-expansions against `g(n)`.
    - The UCS pattern still applies once a state is popped from the queue.
    """

    frontier = utils.PriorityQueue()
    start = problem.getStartState()
    h_start = heuristic(start, problem)
    frontier.push((start, [], 0.0), h_start)  # (node, actions, g), priority=g+h
    visited = {}  # node -> best_g_cost
    
    while not frontier.isEmpty():
        _remember_frontier(problem, frontier)
        node, actions, g = frontier.pop()
        
        # Si ya visitamos este nodo con mejor costo, ignorar
        if node in visited and visited[node] <= g:
            continue
        visited[node] = g
        
        if problem.isGoalState(node):
            return actions
        
        for next_node, action, edge_cost in problem.getSuccessors(node):
            new_g = g + edge_cost
            if next_node not in visited or visited[next_node] > new_g:
                h_next = heuristic(next_node, problem)
                f = new_g + h_next  # g(n) + h(n)
                frontier.push((next_node, actions + [action], new_g), f)
    
    return []


def depthLimitedSearch(problem: SearchProblem, limit: int) -> list[str] | None:
    """Return a solution with at most `limit` actions, or None if none is found.

    Tips:
    - Depth counts actions taken from the start, not recursive calls made.
    - Keep a set of nodes on the current path to avoid revisiting them in one branch.
    """

    frontier = utils.Stack()
    start = problem.getStartState()
    frontier.push((start, [], 0))  # (node, actions, depth)
    on_path = set()
    
    while not frontier.isEmpty():
        _remember_frontier(problem, frontier)
        node, actions, depth = frontier.pop()
        
        if depth > 0 and node in on_path:
            on_path.discard(node)
        
        if problem.isGoalState(node):
            return actions
        
        if depth < limit:
            on_path.add(node)
            for next_node, action, cost in problem.getSuccessors(node):
                if next_node not in on_path:
                    frontier.push((next_node, actions + [action], depth + 1))
    
    return None


def iterativeDeepeningSearch(
    problem: SearchProblem, max_depth: int | None = None
) -> list[str]:
    """Run depth-limited DFS with increasing depth limits.

    Tips:
    - Increase the limit one step at a time and delegate each attempt to DLS.
    - Save the successful depth in `problem._ids_depth_found` before returning.
    """

    if max_depth is None:
        max_depth = 50
    
    for depth_limit in range(max_depth + 1):
        result = depthLimitedSearch(problem, depth_limit)
        if result is not None:
            problem._ids_depth_found = depth_limit
            return result
    
    return []


# Abbreviations used by the CLI and the statement.
dfs = depthFirstSearch
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
