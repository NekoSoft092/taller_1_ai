"""Tests para UCS (Uniform Cost Search)."""

import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from algorithms.search import uniformCostSearch
from algorithms.problems import SearchProblem


class SimpleWeightedProblem(SearchProblem):
    """Un problema con pesos en los arcos."""
    
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


def test_ucs_finds_cheapest_path():
    """UCS debe encontrar el camino con menor costo."""
    print("\n" + "="*70)
    print("TEST: UCS encuentra camino más barato")
    print("="*70)
    
    # Hay dos caminos a C:
    # A -> C directo (costo 10)
    # A -> B -> C (costo 2 + 1 = 3)
    # UCS debería elegir el segundo
    graph = {
        'A': [('C', 'directo_A_C', 10), ('B', 'ir_a_B', 2)],
        'B': [('C', 'ir_a_C', 1)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'C')
    result = uniformCostSearch(problem)
    cost = problem.getCostOfActions(result)
    
    print(f"Camino encontrado: {result}")
    print(f"Costo: {cost}")
    
    # Debería ser el camino más barato (3, no 10)
    assert cost == 3.0, f"UCS debería encontrar costo 3, encontró {cost}"
    print("✓ Pasó: UCS encuentra camino más barato\n")


def test_ucs_vs_bfs():
    """UCS elige por costo, BFS elige por distancia."""
    print("\n" + "="*70)
    print("TEST: UCS vs BFS")
    print("="*70)
    
    # Grafo donde BFS y UCS dan diferentes resultados
    # BFS: A -> B -> D (3 pasos, costo 100)
    # UCS: A -> C -> D (2 pasos, costo 50)
    graph = {
        'A': [('B', 'ir_a_B', 1), ('C', 'ir_a_C', 40)],
        'B': [('D', 'ir_a_D', 99)],
        'C': [('D', 'ir_a_D', 10)],
        'D': []
    }
    
    from algorithms.search import breadthFirstSearch
    
    problem_ucs = SimpleWeightedProblem(graph, 'A', 'D')
    problem_bfs = SimpleWeightedProblem(graph, 'A', 'D')
    
    result_ucs = uniformCostSearch(problem_ucs)
    result_bfs = breadthFirstSearch(problem_bfs)
    
    cost_ucs = problem_ucs.getCostOfActions(result_ucs)
    cost_bfs = problem_bfs.getCostOfActions(result_bfs)
    
    print(f"UCS: {result_ucs} (costo: {cost_ucs})")
    print(f"BFS: {result_bfs} (costo: {cost_bfs})")
    
    assert cost_ucs <= cost_bfs, "UCS debería tener costo <= BFS"
    print("✓ Pasó: UCS encuentra camino más económico\n")


def test_ucs_single_path():
    """UCS en un grafo lineal simple."""
    print("\n" + "="*70)
    print("TEST: UCS en grafo lineal")
    print("="*70)
    
    graph = {
        'A': [('B', 'ir_a_B', 5)],
        'B': [('C', 'ir_a_C', 3)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'C')
    result = uniformCostSearch(problem)
    cost = problem.getCostOfActions(result)
    
    print(f"Camino: {result}")
    print(f"Costo: {cost}")
    
    assert len(result) > 0, "UCS debería encontrar una solución"
    assert cost == 8.0, f"Costo debería ser 8, fue {cost}"
    print("✓ Pasó: UCS calcula costo correcto\n")


def test_ucs_no_solution():
    """UCS cuando no hay solución."""
    print("\n" + "="*70)
    print("TEST: UCS sin solución")
    print("="*70)
    
    graph = {
        'A': [('B', 'ir_a_B', 1)],
        'B': [('C', 'ir_a_C', 1)],
        'C': []
    }
    
    problem = SimpleWeightedProblem(graph, 'A', 'X')
    result = uniformCostSearch(problem)
    
    print(f"Resultado: {result}")
    
    assert result == [], "UCS debería retornar lista vacía si no hay solución"
    print("✓ Pasó: UCS retorna vacío sin solución\n")


def test_ucs_zero_cost():
    """UCS cuando el nodo inicial es el goal."""
    print("\n" + "="*70)
    print("TEST: UCS start = goal")
    print("="*70)
    
    graph = {'A': [('B', 'ir_a_B', 1)]}
    
    problem = SimpleWeightedProblem(graph, 'A', 'A')
    result = uniformCostSearch(problem)
    
    print(f"Resultado: {result}")
    
    assert result == [], "Costo debe ser 0 (lista vacía)"
    print("✓ Pasó: UCS maneja start=goal correctamente\n")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("TESTS PARA UCS (UNIFORM COST SEARCH)")
    print("="*70)
    
    try:
        test_ucs_finds_cheapest_path()
        test_ucs_vs_bfs()
        test_ucs_single_path()
        test_ucs_no_solution()
        test_ucs_zero_cost()
        
        print("\n" + "="*70)
        print("✓ ¡TODOS LOS TESTS DE UCS PASARON!")
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
