# Tests para DFS y BFS

Tests unitarios para las implementaciones de búsqueda en profundidad (DFS) y búsqueda en amplitud (BFS).

## Archivos

- **test_dfs_bfs.py**: Suite de tests básicos para ambos algoritmos
- **test_search_verbose.py**: Tests con información detallada de exploración

## Cómo ejecutar los tests

```bash
# Tests básicos
python tests/test_dfs_bfs.py

# Tests con información detallada (RECOMENDADO para ver el árbol y métricas)
python tests/test_search_verbose.py
```

## Tests básicos (test_dfs_bfs.py)

### DFS (Depth-First Search)
- `test_dfs_simple()`: Verifica que DFS encuentre un camino en un grafo simple
- `test_dfs_no_solution()`: Verifica que retorne lista vacía cuando no hay solución
- `test_dfs_goal_is_start()`: Verifica manejo cuando el goal es el estado inicial

### BFS (Breadth-First Search)
- `test_bfs_simple()`: Verifica que BFS encuentre un camino en un grafo simple
- `test_bfs_no_solution()`: Verifica que retorne lista vacía cuando no hay solución
- `test_bfs_goal_is_start()`: Verifica manejo cuando el goal es el estado inicial

### Comparación
- `test_dfs_shortest_vs_bfs()`: Verifica que BFS encuentra un camino más corto (o igual) que DFS

## Tests con información detallada (test_search_verbose.py)

### Funciones principales

**`dfs_verbose(problem, show_trace=False)`** - DFS con métricas detalladas
```python
actions, metrics = dfs_verbose(problem, show_trace=True)
print_exploration_stats(metrics)     # Estadísticas
print_exploration_order(metrics)     # Orden de exploración
print_search_tree(metrics)            # Árbol de búsqueda
```

**`bfs_verbose(problem, show_trace=False)`** - BFS con métricas detalladas
```python
actions, metrics = bfs_verbose(problem, show_trace=True)
```

### Información disponible en SearchMetrics

- **exploration_order**: Lista con el orden en que se exploraron los nodos
- **tree**: Diccionario con información de cada nodo (padre, acción, profundidad, costo)
- **total_nodes_explored**: Cantidad total de nodos explorados
- **solution_depth**: Profundidad del nodo goal encontrado
- **solution_cost**: Costo acumulado hasta la solución
- **max_frontier_size**: Tamaño máximo que alcanzó la frontera

### Funciones de visualización

**`print_exploration_stats(metrics)`**
Muestra: nodos explorados, profundidad, costo, tamaño máximo de frontera

**`print_exploration_order(metrics, limit=20)`**
Muestra el orden en que se exploraron los nodos (profundidad y acciones)

**`print_search_tree(metrics, max_depth=5)`**
Visualiza el árbol de búsqueda de forma indentada

## Ejemplo de uso

```python
from algorithms.search_verbose import dfs_verbose, print_search_tree
from algorithms.problems import SingleDeliveryProblem
from graph.road_graph import ColombiaRoadGraph

# Cargar grafo y crear problema
graph = ColombiaRoadGraph.from_json("data/colombia_roads.json")
problem = SingleDeliveryProblem(graph, "Bogotá", "Medellín")

# Ejecutar búsqueda con trazado
actions, metrics = dfs_verbose(problem, show_trace=True)

# Ver resultados
print(f"Solución: {actions}")
print(f"Nodos explorados: {metrics.total_nodes_explored}")
print(f"Profundidad: {metrics.solution_depth}")
print_search_tree(metrics, max_depth=4)
```

## Notas de implementación

Ambos algoritmos:
- Usan las estructuras de datos definidas en `algorithms/utils.py` (Stack y Queue)
- Retornan una lista de acciones (strings) que llevan del estado inicial al goal
- Llaman a `_remember_frontier()` para registrar el tamaño máximo de la frontera
- Usan un conjunto de visitados para evitar ciclos

Las versiones verbose adicionales:
- Rastrean el árbol de búsqueda completo (parent, profundidad, costo de cada nodo)
- Pueden mostrar trazado en tiempo real con `show_trace=True`
- Proporcionan métricas detalladas para análisis experimental
