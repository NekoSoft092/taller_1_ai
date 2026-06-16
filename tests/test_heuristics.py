"""Tests para las heurísticas implementadas."""

import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from algorithms.heuristics import (
    nullHeuristic,
    straightLineHeuristic,
    multiDeliveryHeuristic,
    straightLineMultiDeliveryHeuristic,
)
from algorithms.problems import SearchProblem


class SimpleGraphProblem(SearchProblem):
    """Problema simple para testear heurísticas."""
    
    def __init__(self, nodes, edges, start, goal, cost_mode="distance"):
        self.nodes = nodes  # {node_id: (lat, lon)}
        self.edges = edges  # lista de (src, dst, cost)
        self.start = start
        self.goal = goal
        self.cost_mode = cost_mode
        self._expanded = 0
        self.heuristicInfo = {}
    
    def getStartState(self):
        return self.start
    
    def isGoalState(self, state):
        return state == self.goal
    
    def getSuccessors(self, state):
        self._expanded += 1
        successors = []
        for src, dst, cost in self.edges:
            if src == state:
                successors.append((dst, f"ir_a_{dst}", cost))
        return successors
    
    def getCostOfActions(self, actions):
        if not actions:
            return 0.0
        return sum(1.0 for _ in actions)
    
    def coordinates(self, node_id):
        return self.nodes.get(node_id, (0, 0))
    
    class Graph:
        def __init__(self, problem):
            self.problem = problem
        
        def coordinates(self, node_id):
            return self.problem.nodes.get(node_id, (0, 0))
    
    @property
    def graph(self):
        return self.Graph(self)


def test_null_heuristic():
    """Test que nullHeuristic siempre retorna 0."""
    print("\n" + "="*70)
    print("TEST: NULL HEURISTIC")
    print("="*70)
    
    nodes = {'A': (0, 0), 'B': (1, 1), 'C': (2, 2)}
    edges = [('A', 'B', 1), ('B', 'C', 1)]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'C')
    
    h_a = nullHeuristic('A', problem)
    h_b = nullHeuristic('B', problem)
    h_c = nullHeuristic('C', problem)
    
    print(f"h(A) = {h_a}")
    print(f"h(B) = {h_b}")
    print(f"h(C) = {h_c}")
    
    assert h_a == 0.0 and h_b == 0.0 and h_c == 0.0
    print("✓ Pasó: siempre retorna 0")


def test_straight_line_heuristic_distance():
    """Test straightLineHeuristic con modo distance."""
    print("\n" + "="*70)
    print("TEST: STRAIGHT LINE HEURISTIC (distance mode)")
    print("="*70)
    
    # Coordenadas: A en (0,0), B en (0,1), C en (0,2)
    nodes = {'A': (0.0, 0.0), 'B': (1.0, 0.0), 'C': (2.0, 0.0)}
    edges = [('A', 'B', 1), ('B', 'C', 1)]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'C', cost_mode="distance")
    
    h_a = straightLineHeuristic('A', problem)
    h_b = straightLineHeuristic('B', problem)
    h_c = straightLineHeuristic('C', problem)
    
    print(f"h(A) = {h_a:.4f} km")
    print(f"h(B) = {h_b:.4f} km")
    print(f"h(C) = {h_c:.4f} km")
    
    # h(C) debería ser 0 (ya estamos en el goal)
    # h(B) debería ser la distancia geodésica a C
    # h(A) debería ser la distancia geodésica a C
    
    assert h_c < 0.1, "h(goal) debería ser ~0"
    assert h_b < h_a, "h(B) < h(A) porque B está más cerca de C"
    print("✓ Pasó: heurística respeta distancia geodésica")


def test_straight_line_heuristic_stops():
    """Test straightLineHeuristic con modo stops (debería retornar 0)."""
    print("\n" + "="*70)
    print("TEST: STRAIGHT LINE HEURISTIC (stops mode)")
    print("="*70)
    
    nodes = {'A': (0.0, 0.0), 'B': (1.0, 0.0), 'C': (2.0, 0.0)}
    edges = [('A', 'B', 1), ('B', 'C', 1)]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'C', cost_mode="stops")
    
    h_a = straightLineHeuristic('A', problem)
    h_b = straightLineHeuristic('B', problem)
    h_c = straightLineHeuristic('C', problem)
    
    print(f"h(A) = {h_a}")
    print(f"h(B) = {h_b}")
    print(f"h(C) = {h_c}")
    
    assert h_a == 0.0 and h_b == 0.0 and h_c == 0.0
    print("✓ Pasó: retorna 0 en modo stops")


def test_straight_line_multi_delivery():
    """Test straightLineMultiDeliveryHeuristic."""
    print("\n" + "="*70)
    print("TEST: STRAIGHT LINE MULTI-DELIVERY HEURISTIC")
    print("="*70)
    
    nodes = {
        'A': (0.0, 0.0),
        'B': (1.0, 0.0),
        'C': (2.0, 0.0),
        'D': (3.0, 0.0),
    }
    edges = [
        ('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1),
        ('B', 'D', 2), ('A', 'C', 2)
    ]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'D')
    
    # Estado: (nodo actual, entregas pendientes)
    state_a = ('A', frozenset(['C', 'D']))
    state_b = ('B', frozenset(['C', 'D']))
    state_c = ('C', frozenset(['D']))
    state_d = ('D', frozenset())
    
    h_a = straightLineMultiDeliveryHeuristic(state_a, problem)
    h_b = straightLineMultiDeliveryHeuristic(state_b, problem)
    h_c = straightLineMultiDeliveryHeuristic(state_c, problem)
    h_d = straightLineMultiDeliveryHeuristic(state_d, problem)
    
    print(f"h(A, {{C,D}}) = {h_a:.4f}")
    print(f"h(B, {{C,D}}) = {h_b:.4f}")
    print(f"h(C, {{D}}) = {h_c:.4f}")
    print(f"h(D, {{}}) = {h_d:.4f}")
    
    assert h_d == 0.0, "h(goal, {}) debería ser 0"
    assert h_c < h_b < h_a, "heurística debería disminuir con entregas visitadas"
    print("✓ Pasó: heurística decrece correctamente")


def test_heuristic_admissibility():
    """Test que las heurísticas sean admisibles (h disminuye hacia goal)."""
    print("\n" + "="*70)
    print("TEST: ADMISSIBILITY (h decrece hacia goal)")
    print("="*70)
    
    # Usar coordenadas en línea recta
    nodes = {
        'A': (4.0, -74.0),      # Inicio
        'B': (5.0, -74.5),      # Intermedio
        'C': (6.0, -75.0)       # Goal
    }
    edges = [('A', 'B', 10), ('B', 'C', 10), ('A', 'C', 25)]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'C', cost_mode="distance")
    
    h_a = straightLineHeuristic('A', problem)
    h_b = straightLineHeuristic('B', problem)
    h_c = straightLineHeuristic('C', problem)
    
    print(f"h(A) = {h_a:.4f} km")
    print(f"h(B) = {h_b:.4f} km")
    print(f"h(C) = {h_c:.4f} km")
    
    # En línea recta, h debería disminuir monotónicamente
    assert h_c == 0.0, "h(goal) debe ser 0"
    assert h_b > 0, "h(B) debe ser > 0"
    assert h_a > h_b, "h(A) debe ser > h(B) pues A está más lejos"
    print("✓ Pasó: heurística decrece acercándose al goal")


def test_comparison():
    """Comparar el valor de diferentes heurísticas."""
    print("\n" + "="*70)
    print("COMPARACIÓN DE HEURÍSTICAS")
    print("="*70)
    
    nodes = {'A': (0.0, 0.0), 'B': (1.0, 0.0), 'C': (2.0, 0.0)}
    edges = [('A', 'B', 1), ('B', 'C', 1)]
    problem = SimpleGraphProblem(nodes, edges, 'A', 'C', cost_mode="distance")
    
    h_null = nullHeuristic('A', problem)
    h_straight = straightLineHeuristic('A', problem)
    
    print(f"Desde A hacia C:")
    print(f"  Null heuristic: {h_null}")
    print(f"  Straight line:  {h_straight:.4f}")
    
    print(f"\nInterpretación:")
    print(f"  - Null: no da información (A* = Dijkstra)")
    print(f"  - Straight line: da información sobre dirección")
    
    assert h_null <= h_straight, "null <= straight line siempre"
    print("✓ Pasó: Null es menos informativo que straight line")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("EJECUTANDO TESTS DE HEURÍSTICAS")
    print("="*70)
    
    try:
        test_null_heuristic()
        test_straight_line_heuristic_distance()
        test_straight_line_heuristic_stops()
        test_straight_line_multi_delivery()
        test_heuristic_admissibility()
        test_comparison()
        
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
