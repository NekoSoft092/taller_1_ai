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

    ### YOUR CODE HERE ###
    nodo_comienzo= problem.getStartState()
    pila_info=utils.Stack()
    pila_info.push((nodo_comienzo, [], set()))
    _remember_frontier(problem, pila_info)
    
    while not pila_info.isEmpty():
        nodo_actual,acciones,visitados=pila_info.pop()
        _remember_frontier(problem, pila_info)
        if problem.isGoalState(nodo_actual):
            return acciones
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for nodo_siguiente, accion, costo in problem.getSuccessors(nodo_actual):
                pila_info.push((nodo_siguiente, acciones+[accion], visitados))
                #Herramienta de IA recomendó vistados.copy() pero al probarlo resultaba en un posible bucle infinito, se probó durante 15 minutos y no paraba la ejecución.
                _remember_frontier(problem, pila_info)
    
    return []
    ### END YOUR CODE ###


def breadthFirstSearch(problem: SearchProblem) -> list[str]:
    """Search the shallowest nodes in the search tree first.

    Tips:
    - Mark a state as visited when you enqueue it, not when you dequeue it.
    - Test for the goal immediately after dequeuing a state.
    """

    ### YOUR CODE HERE ###
    nodo_comienzo = problem.getStartState()
    cola_info = utils.Queue()
    visitados = set()
    
    cola_info.push((nodo_comienzo, []))
    visitados.add(nodo_comienzo)
    _remember_frontier(problem, cola_info)
    
    while not cola_info.isEmpty():
        nodo_actual, acciones = cola_info.pop()
        _remember_frontier(problem, cola_info)
        if problem.isGoalState(nodo_actual):
            return acciones
        for nodo_siguiente, accion, costo in problem.getSuccessors(nodo_actual):
            if nodo_siguiente not in visitados:
                visitados.add(nodo_siguiente)
                cola_info.push((nodo_siguiente, acciones + [accion]))
                _remember_frontier(problem, cola_info)
    
    return []
    ### END YOUR CODE ###


def uniformCostSearch(problem: SearchProblem) -> list[str]:
    ### YOUR CODE HERE ###

    # Primera Interación, Inspirada en el Código Base de GeeksforGeeks
    # https://www.geeksforgeeks.org/artificial-intelligence/uniform-cost-search-ucs-in-ai/
    # ------------------------------------------------------------
    # priority_queue = [(0, start)]
    # visited = {start: (0, None)}
    #
    # while priority_queue:
    #     current_cost, current_node = heapq.heappop(priority_queue)
    #
    #     if current_node == goal:
    #         return current_cost, reconstruct_path(visited, start, goal)
    #
    #     for neighbor, cost in graph[current_node]:
    #         total_cost = current_cost + cost
    #         if neighbor not in visited or total_cost < visited[neighbor][0]:
    #             visited[neighbor] = (total_cost, current_node)
    #             heapq.heappush(priority_queue, (total_cost, neighbor))
    # return None
    #
    # Cambios realizados:
    # Se identificaron los choques entre el codigo base de GeeksforGeeks
    # y los objetos del framework del proyecto (librerias).
    # Implementación:
    # 1. Se cambio el "heapq" a "utils.PriorityQueue()".
    # 2. Se cambió "graph[nodo]" por "problem.getSuccessors(estado)".
    # 3. Se eliminó la necesidad de usar un reconstruct_path
    # ------------------------------------------------------------
    # Versión Preliminar, Antes de Cambios Finales:
    # ------------------------------------------------------------
    # frontera = utils.PriorityQueue()
    # mejor_costo = {}
    # inicio = problem.getStartState()
    # mejor_costo[inicio] = 0
    # frontera.push((inicio, 0), 0)
    # while not frontera.isEmpty():
    #     estado, g = frontera.pop()
    #
    #     if problem.isGoalState(estado):
    #         return estado
    #
    #     for sucesor, accion, costo_paso in problem.getSuccessors(estado):
    #         nuevo_g = g + costo_paso
    #         if nuevo_g < mejor_costo.get(sucesor, float("inf")):
    #             mejor_costo[sucesor] = nuevo_g
    #             frontera.push((sucesor, nuevo_g), nuevo_g)
    #
    # Prompt Usado Con Herramienta IA:
    # "Tengo este código adaptado de GeeksforGeeks que ya maneja el costo g
    # y los sucesores del proyecto, pero necesito ayuda para ajustarlo bien.
    # No sé cómo hacer para que me regrese la lista del camino de acciones.
    # Si vez otro detalle que pueda dar un probleam al probar avisame."
    # ------------------------------------------------------------
    # Versión final
    frontera = utils.PriorityQueue()
    mejor_costo = {}

    inicio = problem.getStartState()
    mejor_costo[inicio] = 0
    frontera.push((inicio, [], 0), 0)

    while not frontera.isEmpty():
        estado, acciones, g = frontera.pop()

        if g > mejor_costo.get(estado, float("inf")):
            continue
        if problem.isGoalState(estado):
            return acciones

        for sucesor, accion, costo_paso in problem.getSuccessors(estado):
            nuevo_g = g + costo_paso

            if nuevo_g < mejor_costo.get(sucesor, float("inf")):
                mejor_costo[sucesor] = nuevo_g
                frontera.push((sucesor, acciones + [accion], nuevo_g), nuevo_g)

        _remember_frontier(problem, frontera)
    return []
    ### END YOUR CODE ###

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> list[str]:
    """Search the node with the lowest `g(n) + h(n)` first.

    Tips:
    - Push `g(n) + h(n)` to the frontier, but compare re-expansions against `g(n)`.
    - The UCS pattern still applies once a state is popped from the queue.
    """

    ### YOUR CODE HERE ###
    frontera = utils.PriorityQueue()
    estadoInicial = problem.getStartState()
    costos_g = {estadoInicial: 0}
    prioridadInicial = 0 + heuristic(estadoInicial, problem)
    
    frontera.push((estadoInicial, [], 0.0), prioridadInicial)
    
    while not frontera.isEmpty():
        estadoActual, caminoActual, gActual = frontera.pop()
        
        if problem.isGoalState(estadoActual):
            return caminoActual
            
        if gActual > costos_g.get(estadoActual, float('inf')):
            continue
            
        for siguienteEstado, accion, costoTramo in problem.getSuccessors(estadoActual):
            nuevo_g = gActual + costoTramo
            
            if siguienteEstado not in costos_g or nuevo_g < costos_g[siguienteEstado]:
                costos_g[siguienteEstado] = nuevo_g
                prioridad_f = nuevo_g + heuristic(siguienteEstado, problem)
                nuevoCamino = caminoActual + [accion]
                frontera.push((siguienteEstado, nuevoCamino, nuevo_g), prioridad_f)
                
    return []
    ### END YOUR CODE ###


def depthLimitedSearch(problem: SearchProblem, limit: int) -> list[str] | None:
    """Return a solution with at most `limit` actions, or None if none is found.

    Tips:
    - Depth counts actions taken from the start, not recursive calls made.
    - Keep a set of nodes on the current path to avoid revisiting them in one branch.
    """
    # Implementación en pseudocódigo de https://www.geeksforgeeks.org/artificial-intelligence/depth-limited-search-for-ai/  con la que se iteró con la herramienta de IA.
    #def depth_limited_search(node, goal_test, limit):
    #if goal_test(node):
    #   return node
    #elif limit == 0:
    #    return "cutoff"
    #else:
    #    cutoff_occurred = False
    #    for child in expand(node):
    #        result = depth_limited_search(child, goal_test, limit - 1)
    #        if result == "cutoff":
    #            cutoff_occurred = True
    #        elif result != "failure":
    #            return result
    #    return "cutoff" if cutoff_occurred else "failure"
    # Prompt Usado Con Herramienta IA: Teniendo en cuenta el pseudocódigo compartido y el contexto del problema, 
    # ayúdame a adaptar el código teniendo en cuenta que: (1) La función recibe un problem y un límite, no un nodo. 
    # (2) La función deber retornar la lista de acciones tomada, o None si no se encuentra solución dentro del límite. 
    # (3) Se utiliza getSuccessors para expandir los nodos. 
    # (4) No se admiten ciclos en la rama actual.
    ### YOUR CODE HERE ###
    def recursive_dls(nodo, acciones, visitados_rama, limite_actual):
        if problem.isGoalState(nodo):
            return acciones
        if limite_actual == 0:
            return None
        for nodo_siguiente, accion, costo in problem.getSuccessors(nodo):
            if nodo_siguiente not in visitados_rama:
                visitados_rama.add(nodo_siguiente)
                resultado = recursive_dls(nodo_siguiente, acciones + [accion], visitados_rama, limite_actual - 1)
                if resultado is not None:
                    return resultado
                visitados_rama.remove(nodo_siguiente)
        return None

    nodo_inicio = problem.getStartState()
    return recursive_dls(nodo_inicio, [], {nodo_inicio}, limit)
    ### END YOUR CODE ###
    # Cambios del pseudocódigo a la implementación
    #1. El pseudocódigo recibe el nodo directamente. Aquí se obtiene con problem.getStartState() y se pasa a la función recursiva.
    #2. El pseudocódigo retorna "cutoff" o "failure" como strings. Aquí se retorna la lista de acciones si encuentra la meta, o None si no encuentra solución.
    #3. El pseudocódigo usa goal_test(node). Aquí se usa problem.isGoalState(nodo).
    #4. El pseudocódigo usa expand(node). Aquí se usa problem.getSuccessors(nodo) que devuelve tripletas (nodo_siguiente, accion, costo).
    #5. El pseudocódigo no rastrea el camino. Aquí se pasa acciones + [accion] en cada llamada recursiva para construir la ruta.
    #6. El pseudocódigo no evita ciclos. Aquí se usa visitados_rama que se agrega al entrar a un nodo y se elimina al retroceder, garantizando que solo se evitan ciclos dentro de la rama actual.


def iterativeDeepeningSearch(
    problem: SearchProblem, max_depth: int | None = None
) -> list[str]:
    """Run depth-limited DFS with increasing depth limits.

    Tips:
    - Increase the limit one step at a time and delegate each attempt to DLS.
    - Save the successful depth in `problem._ids_depth_found` before returning.
    """

    ### YOUR CODE HERE ###
    depth = 0
    while max_depth is None or depth <= max_depth:
        resultado = depthLimitedSearch(problem, depth)
        if resultado is not None:
            problem._ids_depth_found = depth
            return resultado
        depth += 1
    
    return []
    ### END YOUR CODE ###


# Abbreviations used by the CLI and the statement.
dfs = depthFirstSearch
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
