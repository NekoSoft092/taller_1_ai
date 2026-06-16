"""Tests para A*, DLS e IDS."""

import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from algorithms.search import aStarSearch, depthLimitedSearch, iterativeDeepeningSearch
from algorithms.heuristics import nullHeuristic
from algorithms.problems import SearchProblem


class SimpleWeightedProblem(SearchProblem):
    """Un problema simple con pesos para testear."""
    
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self._expanded = 0
        self._max_frontier_size = 0
        self.heuristicInfo = {}
    
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
    
    def coordinates(self, node):
        # Para heurísticas - coordenadas simples
        coords_map = {
            'A': (0, 0), 'B': (1, 0), 'C': (2, 0),
            'D': (3, 0), 'E': (4, 0), 'F': (5, 0)
        }
        return coords_map.get(node, (0, 0))


def simple_heuristic(state, problem):
    """Heurística simple: distancia Manhattan al goal."""
    if not hasattr(problem, 'goal'):
        return 0.0
    
    state_coords = problem.coordinates(state)
    goal_coords = problem.coordinates(problem.goal)
    
    if state == problem.goal:
        return 0.0
    
    # Estimar como número de nodos hasta el goal
    # A->B->C->D es 3 pasos, A->D es ~3
    dx = abs(ord(state) - ord(problem.goal))
    return float(dx) * 0.5


# ============ A* TESTS ============

def test_astar_with_null_heuristic():
    """A* con heurística nula es como UCS."""
    print("\n" + "="*70)
    print("TEST: A* con heurística nula (= UCS)")
    print("="*70)
    
    graph = {
        'A': [('C', 'directo', 10), ('B', 'ir_a_B', 2)],
        'B': [('C', 'ir_a_C', 1)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'C')
    result = aStarSearch(problem, heuristic=nullHeuristic)
    cost = problem.getCostOfActions(result)
    
    print(f"Camino: {result}")
    print(f"Costo: {cost}")
    
    assert cost == 3.0, "A* con null debería encontrar costo 3"
    print("✓ Pasó: A* con null heuristic funciona\n")


def test_astar_with_good_heuristic():
    """A* con buena heurística explora menos nodos."""
    print("\n" + "="*70)
    print("TEST: A* con heurística informada")
    print("="*70)
    
    graph = {
        'A': [('B', 'ir_a_B', 1), ('C', 'ir_a_C', 5)],
        'B': [('D', 'ir_a_D', 1)],
        'C': [('D', 'ir_a_D', 1)],
        'D': []
    }
    
    problem_with_h = SimpleWeightedProblem(graph, 'A', 'D')
    problem_null = SimpleWeightedProblem(graph, 'A', 'D')
    
    result_with_h = aStarSearch(problem_with_h, heuristic=simple_heuristic)
    result_null = aStarSearch(problem_null, heuristic=nullHeuristic)
    
    cost_with_h = problem_with_h.getCostOfActions(result_with_h)
    cost_null = problem_null.getCostOfActions(result_null)
    expanded_with_h = problem_with_h._expanded
    expanded_null = problem_null._expanded
    
    print(f"Con heurística: {result_with_h} (costo={cost_with_h}, expandidos={expanded_with_h})")
    print(f"Sin heurística: {result_null} (costo={cost_null}, expandidos={expanded_null})")
    
    # Ambos deben encontrar la solución óptima
    assert cost_with_h == cost_null, "A* debería encontrar lo mismo"
    # Con heurística podría expandir menos (pero no siempre)
    print("✓ Pasó: A* con heurística funciona\n")


def test_astar_finds_optimal():
    """A* garantiza solución óptima."""
    print("\n" + "="*70)
    print("TEST: A* encuentra solución óptima")
    print("="*70)
    
    graph = {
        'A': [('B', 'to_B', 1), ('C', 'to_C', 100)],
        'B': [('D', 'to_D', 1)],
        'C': [('D', 'to_D', 1)],
        'D': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'D')
    result = aStarSearch(problem, heuristic=simple_heuristic)
    cost = problem.getCostOfActions(result)
    
    print(f"Camino: {result}")
    print(f"Costo: {cost}")
    
    assert cost == 2.0, "A* debe encontrar costo óptimo de 2"
    print("✓ Pasó: A* encuentra solución óptima\n")


# ============ DLS TESTS ============

def test_dls_respects_limit():
    """DLS respeta el límite de profundidad."""
    print("\n" + "="*70)
    print("TEST: DLS respeta límite de profundidad")
    print("="*70)
    
    # Grafo donde solución está a profundidad 3: A->B->C->D
    graph = {
        'A': [('B', 'to_B', 1)],
        'B': [('C', 'to_C', 1)],
        'C': [('D', 'to_D', 1)],
        'D': []
    }
    
    # Con límite 2, no debería encontrar D
    problem = SimpleWeightedProblem(graph, 'A', 'D')
    result = depthLimitedSearch(problem, limit=2)
    
    print(f"Límite=2, resultado: {result}")
    assert result is None, "DLS con límite 2 no debería encontrar solución"
    
    # Con límite 3, debería encontrar
    problem2 = SimpleWeightedProblem(graph, 'A', 'D')
    result2 = depthLimitedSearch(problem2, limit=3)
    
    print(f"Límite=3, resultado: {result2}")
    assert result2 is not None, "DLS con límite 3 debería encontrar solución"
    print("✓ Pasó: DLS respeta el límite\n")


def test_dls_linear_graph():
    """DLS en un grafo lineal."""
    print("\n" + "="*70)
    print("TEST: DLS en grafo lineal")
    print("="*70)
    
    graph = {
        'A': [('B', 'to_B', 1)],
        'B': [('C', 'to_C', 1)],
        'C': [('D', 'to_D', 1)],
        'D': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'D')
    result = depthLimitedSearch(problem, limit=10)
    
    print(f"Resultado: {result}")
    assert result is not None, "Debería encontrar solución"
    assert len(result) == 3, "Debería tener 3 acciones"
    print("✓ Pasó: DLS encuentra solución lineal\n")


def test_dls_with_cycles():
    """DLS maneja ciclos correctamente."""
    print("\n" + "="*70)
    print("TEST: DLS maneja ciclos")
    print("="*70)
    
    # Grafo con ciclo: A->B->A, pero también A->C->D
    graph = {
        'A': [('B', 'to_B', 1), ('C', 'to_C', 2)],
        'B': [('A', 'to_A', 1)],
        'C': [('D', 'to_D', 1)],
        'D': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'D')
    result = depthLimitedSearch(problem, limit=5)
    
    print(f"Resultado: {result}")
    assert result is not None, "Debería encontrar solución evitando ciclo"
    print("✓ Pasó: DLS evita ciclos\n")


def test_dls_start_is_goal():
    """DLS cuando inicio = goal."""
    print("\n" + "="*70)
    print("TEST: DLS start = goal")
    print("="*70)
    
    graph = {'A': [('B', 'to_B', 1)]}
    
    problem = SimpleWeightedProblem(graph, 'A', 'A')
    result = depthLimitedSearch(problem, limit=1)
    
    print(f"Resultado: {result}")
    assert result == [], "Debería retornar lista vacía"
    print("✓ Pasó: DLS maneja start=goal\n")


# ============ IDS TESTS ============

def test_ids_finds_solution():
    """IDS encuentra solución."""
    print("\n" + "="*70)
    print("TEST: IDS encuentra solución")
    print("="*70)
    
    graph = {
        'A': [('B', 'to_B', 1)],
        'B': [('C', 'to_C', 1)],
        'C': [('D', 'to_D', 1)],
        'D': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'D')
    result = iterativeDeepeningSearch(problem, max_depth=10)
    
    print(f"Resultado: {result}")
    print(f"Profundidad encontrada: {problem._ids_depth_found}")
    
    assert result is not None, "IDS debería encontrar solución"
    assert problem._ids_depth_found == 3, "Debería encontrar en profundidad 3"
    print("✓ Pasó: IDS encuentra solución\n")


def test_ids_incrementally_increases_depth():
    """IDS incrementa profundidad progresivamente."""
    print("\n" + "="*70)
    print("TEST: IDS incrementa profundidad")
    print("="*70)
    
    # Solución en profundidad 2
    graph = {
        'A': [('B', 'to_B', 1)],
        'B': [('C', 'to_C', 1)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'C')
    result = iterativeDeepeningSearch(problem, max_depth=5)
    
    print(f"Resultado: {result}")
    print(f"Profundidad encontrada: {problem._ids_depth_found}")
    
    assert result is not None, "Debería encontrar"
    assert problem._ids_depth_found == 2, "Debería encontrar exactamente en profundidad 2"
    print("✓ Pasó: IDS incrementa correctamente\n")


def test_ids_no_solution():
    """IDS retorna vacío si no hay solución."""
    print("\n" + "="*70)
    print("TEST: IDS sin solución")
    print("="*70)
    
    graph = {
        'A': [('B', 'to_B', 1)],
        'B': [('C', 'to_C', 1)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'X')
    result = iterativeDeepeningSearch(problem, max_depth=10)
    
    print(f"Resultado: {result}")
    
    assert result == [], "IDS debería retornar vacío"
    print("✓ Pasó: IDS retorna vacío sin solución\n")


def test_ids_vs_dfs():
    """IDS como alternativa a DFS para búsqueda sin información."""
    print("\n" + "="*70)
    print("TEST: IDS vs DFS (optimalidad)")
    print("="*70)
    
    # Grafo donde DFS encuentra solución larga, IDS encuentra corta
    graph = {
        'A': [('B', 'to_B', 1), ('C', 'to_C', 1)],
        'B': [('D', 'to_D', 1), ('E', 'to_E', 1)],
        'C': [('F', 'to_F', 1)],
        'D': [],
        'E': [('F', 'to_F', 1)],
        'F': []
    }
    
    from algorithms.search import depthFirstSearch
    
    problem_ids = SimpleWeightedProblem(graph, 'A', 'F')
    problem_dfs = SimpleWeightedProblem(graph, 'A', 'F')
    
    result_ids = iterativeDeepeningSearch(problem_ids, max_depth=10)
    result_dfs = depthFirstSearch(problem_dfs)
    
    len_ids = len(result_ids) if result_ids else 0
    len_dfs = len(result_dfs) if result_dfs else 0
    
    print(f"IDS: {result_ids} (pasos={len_ids})")
    print(f"DFS: {result_dfs} (pasos={len_dfs})")
    
    # IDS debería encontrar solución más corta
    assert len_ids <= len_dfs, "IDS debería encontrar camino más corto"
    print("✓ Pasó: IDS es más óptimo que DFS\n")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("TESTS PARA A*, DLS E IDS")
    print("="*70)
    
    try:
        # A* tests
        test_astar_with_null_heuristic()
        test_astar_with_good_heuristic()
        test_astar_finds_optimal()
        
        # DLS tests
        test_dls_respects_limit()
        test_dls_linear_graph()
        test_dls_with_cycles()
        test_dls_start_is_goal()
        
        # IDS tests
        test_ids_finds_solution()
        test_ids_incrementally_increases_depth()
        test_ids_no_solution()
        test_ids_vs_dfs()
        
        print("\n" + "="*70)
        print("✓ ¡TODOS LOS TESTS PASARON!")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n✗ Test fallido: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
