"""Tests para DFS y BFS"""

import sys
from pathlib import Path

# Agregar el root del proyecto al path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from algorithms.search import depthFirstSearch, breadthFirstSearch
from algorithms.problems import SearchProblem


class SimpleMazeProblem(SearchProblem):
    """Un problema simple de laberinto para testear."""
    
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self._expanded = 0
        self._max_frontier_size = 0
    
    def getStartState(self):
        return self.start
    
    def isGoalState(self, state):
        return state == self.goal
    
    def getSuccessors(self, state):
        self._expanded += 1
        successors = []
        if state in self.graph:
            for next_state, action, cost in self.graph[state]:
                successors.append((next_state, action, cost))
        return successors
    
    def getCostOfActions(self, actions):
        if actions is None:
            return float('inf')
        cost = 0
        current = self.start
        for action in actions:
            found = False
            for next_state, act, c in self.graph.get(current, []):
                if act == action:
                    cost += c
                    current = next_state
                    found = True
                    break
            if not found:
                return float('inf')
        return cost


def test_dfs_simple():
    """DFS en un grafo simple."""
    graph = {
        'A': [('B', 'go_to_B', 1), ('C', 'go_to_C', 1)],
        'B': [('D', 'go_to_D', 1)],
        'C': [('E', 'go_to_E', 1)],
        'D': [],
        'E': [('F', 'go_to_F', 1)],
        'F': []
    }
    
    problem = SimpleMazeProblem(graph, 'A', 'F')
    result = depthFirstSearch(problem)
    
    print(f"DFS test simple:")
    print(f"  Resultado: {result}")
    print(f"  Goal alcanzado: {problem.isGoalState('F') and result}")
    assert len(result) > 0, "DFS debería encontrar una solución"
    assert result[-1] == 'go_to_F', "El último paso debería llevar a F"
    print("  ✓ Pasó\n")


def test_bfs_simple():
    """BFS en un grafo simple."""
    graph = {
        'A': [('B', 'go_to_B', 1), ('C', 'go_to_C', 1)],
        'B': [('D', 'go_to_D', 1)],
        'C': [('E', 'go_to_E', 1)],
        'D': [],
        'E': [('F', 'go_to_F', 1)],
        'F': []
    }
    
    problem = SimpleMazeProblem(graph, 'A', 'F')
    result = breadthFirstSearch(problem)
    
    print(f"BFS test simple:")
    print(f"  Resultado: {result}")
    print(f"  Goal alcanzado: {problem.isGoalState('F') and result}")
    assert len(result) > 0, "BFS debería encontrar una solución"
    assert result[-1] == 'go_to_F', "El último paso debería llevar a F"
    print("  ✓ Pasó\n")


def test_dfs_no_solution():
    """DFS cuando no hay solución."""
    graph = {
        'A': [('B', 'go_to_B', 1)],
        'B': [('C', 'go_to_C', 1)],
        'C': []
    }
    
    problem = SimpleMazeProblem(graph, 'A', 'X')
    result = depthFirstSearch(problem)
    
    print(f"DFS test sin solución:")
    print(f"  Resultado: {result}")
    assert result == [], "DFS debería retornar lista vacía si no hay solución"
    print("  ✓ Pasó\n")


def test_bfs_no_solution():
    """BFS cuando no hay solución."""
    graph = {
        'A': [('B', 'go_to_B', 1)],
        'B': [('C', 'go_to_C', 1)],
        'C': []
    }
    
    problem = SimpleMazeProblem(graph, 'A', 'X')
    result = breadthFirstSearch(problem)
    
    print(f"BFS test sin solución:")
    print(f"  Resultado: {result}")
    assert result == [], "BFS debería retornar lista vacía si no hay solución"
    print("  ✓ Pasó\n")


def test_dfs_goal_is_start():
    """DFS cuando el goal es el estado inicial."""
    graph = {'A': [('B', 'go_to_B', 1)]}
    
    problem = SimpleMazeProblem(graph, 'A', 'A')
    result = depthFirstSearch(problem)
    
    print(f"DFS test goal = start:")
    print(f"  Resultado: {result}")
    assert result == [], "DFS debería retornar lista vacía si start es goal"
    print("  ✓ Pasó\n")


def test_bfs_goal_is_start():
    """BFS cuando el goal es el estado inicial."""
    graph = {'A': [('B', 'go_to_B', 1)]}
    
    problem = SimpleMazeProblem(graph, 'A', 'A')
    result = breadthFirstSearch(problem)
    
    print(f"BFS test goal = start:")
    print(f"  Resultado: {result}")
    assert result == [], "BFS debería retornar lista vacía si start es goal"
    print("  ✓ Pasó\n")


def test_dfs_shortest_vs_bfs():
    """Comparar DFS y BFS - BFS debería encontrar camino más corto."""
    # Grafo con múltiples caminos
    graph = {
        'A': [('B', 'to_B', 1), ('C', 'to_C', 1)],
        'B': [('D', 'to_D', 1), ('E', 'to_E', 1)],
        'C': [('E', 'to_E_via_C', 1)],
        'D': [],
        'E': []
    }
    
    dfs_problem = SimpleMazeProblem(graph, 'A', 'E')
    bfs_problem = SimpleMazeProblem(graph, 'A', 'E')
    
    dfs_result = depthFirstSearch(dfs_problem)
    bfs_result = breadthFirstSearch(bfs_problem)
    
    print(f"DFS vs BFS:")
    print(f"  DFS resultado: {dfs_result} (len={len(dfs_result)})")
    print(f"  BFS resultado: {bfs_result} (len={len(bfs_result)})")
    print(f"  BFS es más corto: {len(bfs_result) <= len(dfs_result)}")
    # BFS debería ser más corto o igual en términos de número de pasos
    assert len(bfs_result) <= len(dfs_result), "BFS debería encontrar camino más corto"
    print("  ✓ Pasó\n")


if __name__ == '__main__':
    print("=" * 50)
    print("Ejecutando tests para DFS y BFS")
    print("=" * 50 + "\n")
    
    try:
        test_dfs_simple()
        test_bfs_simple()
        test_dfs_no_solution()
        test_bfs_no_solution()
        test_dfs_goal_is_start()
        test_bfs_goal_is_start()
        test_dfs_shortest_vs_bfs()
        
        print("=" * 50)
        print("✓ Todos los tests pasaron!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ Test fallido: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
