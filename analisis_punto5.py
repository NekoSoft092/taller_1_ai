"""
Análisis experimental del Punto 5: Entregas Múltiples
Comparación de A* con multiDeliveryHeuristic vs nullHeuristic
"""

import json
import time
import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from algorithms.search import aStarSearch
from algorithms.heuristics import nullHeuristic, multiDeliveryHeuristic
from algorithms.problems import MultiDeliveryProblem
from graph.road_graph import ColombiaRoadGraph


class ExperimentResults:
    """Almacena resultados de un experimento."""
    
    def __init__(self, name, heuristic_name):
        self.name = name
        self.heuristic_name = heuristic_name
        self.cost = 0.0
        self.actions = 0
        self.expanded = 0
        self.frontier_max = 0
        self.time = 0.0
        self.success = False


def load_instances(instances_path):
    """Carga las instancias del archivo JSON."""
    with open(instances_path) as f:
        data = json.load(f)
    return data


def run_experiment(graph, instance_name, deliveries, heuristic_fn, heuristic_name):
    """Ejecuta un experimento individual."""
    result = ExperimentResults(instance_name, heuristic_name)
    
    try:
        problem = MultiDeliveryProblem(graph, "n1037511", deliveries)
        
        start_time = time.perf_counter()
        actions = aStarSearch(problem, heuristic=heuristic_fn)
        elapsed = time.perf_counter() - start_time
        
        result.time = elapsed
        result.actions = len(actions) if actions else 0
        result.cost = problem.getCostOfActions(actions)
        result.expanded = problem._expanded
        result.frontier_max = getattr(problem, '_max_frontier_size', 0)
        result.success = result.cost < float('inf')
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return result


def print_results_table(results_dict):
    """Imprime tabla de resultados en formato markdown."""
    
    for instance_name, results_list in results_dict.items():
        print(f"\n{'='*100}")
        print(f"INSTANCIA: {instance_name}")
        print('='*100)
        print(f"\n{'Algoritmo':<35} {'Costo (km)':<12} {'Tramos':<8} {'Expandidos':<12} {'Frontera':<10} {'Tiempo (s)':<12}")
        print('-'*100)
        
        for result in results_list:
            algo = f"A* ({result.heuristic_name})"
            costo = f"{result.cost:.2f}" if result.success else "ERROR"
            tramos = str(result.actions)
            expandidos = str(result.expanded)
            frontera = str(result.frontier_max)
            tiempo = f"{result.time:.4f}"
            
            print(f"{algo:<35} {costo:<12} {tramos:<8} {expandidos:<12} {frontera:<10} {tiempo:<12}")
        
        # Análisis
        if len(results_list) >= 2:
            null_res = results_list[0]
            multi_res = results_list[1]
            
            if null_res.success and multi_res.success:
                expansion_ratio = (1 - multi_res.expanded / null_res.expanded) * 100 if null_res.expanded > 0 else 0
                time_ratio = (1 - multi_res.time / null_res.time) * 100 if null_res.time > 0 else 0
                
                print(f"\n📊 Análisis de mejora:")
                print(f"  • Reducción de nodos expandidos: {expansion_ratio:.1f}%")
                print(f"  • Reducción de tiempo: {time_ratio:.1f}%")
                
                if expansion_ratio > 0:
                    print(f"  ✓ multiDeliveryHeuristic es más eficiente que nullHeuristic")
                else:
                    print(f"  ! Ambas heurísticas tienen similar rendimiento")


def run_all_experiments(graph_path, instances_path):
    """Ejecuta todos los experimentos."""
    
    print("\n" + "="*100)
    print("PUNTO 5: ANÁLISIS DE ENTREGAS MÚLTIPLES")
    print("="*100)
    print(f"Grafo: {graph_path}")
    print(f"Instancias: {instances_path}")
    
    # Cargar grafo
    print("\n📂 Cargando grafo...")
    graph = ColombiaRoadGraph.from_json(graph_path)
    print(f"  ✓ {len(graph.nodes)} nodos, {sum(len(edges) for edges in graph.adjacency.values())} aristas")
    
    # Cargar instancias
    print("\n📋 Cargando instancias...")
    instances = load_instances(instances_path)
    
    # Ejecutar experimentos
    results_dict = {}
    
    for instance_type in ['multi']:
        matching_instances = {k: v for k, v in instances.items() if k.startswith(instance_type)}
        
        if not matching_instances:
            print(f"  ⚠ No hay instancias de tipo '{instance_type}'")
            continue
        
        for instance_name, instance_data in matching_instances.items():
            print(f"\n🔍 Procesando: {instance_name}")
            deliveries = instance_data.get('deliveries', [])
            print(f"  Entregas: {len(deliveries)} puntos")
            
            results_dict[instance_name] = []
            
            # Ejecutar con nullHeuristic
            print(f"  → A* (nullHeuristic)...", end=" ", flush=True)
            result_null = run_experiment(graph, instance_name, deliveries, nullHeuristic, "nullHeuristic")
            results_dict[instance_name].append(result_null)
            
            if result_null.success:
                print(f"✓ (costo={result_null.cost:.2f}, expandidos={result_null.expanded}, tiempo={result_null.time:.4f}s)")
            else:
                print(f"✗")
            
            # Ejecutar con multiDeliveryHeuristic
            print(f"  → A* (multiDeliveryHeuristic)...", end=" ", flush=True)
            result_multi = run_experiment(graph, instance_name, deliveries, multiDeliveryHeuristic, "multiDeliveryHeuristic")
            results_dict[instance_name].append(result_multi)
            
            if result_multi.success:
                print(f"✓ (costo={result_multi.cost:.2f}, expandidos={result_multi.expanded}, tiempo={result_multi.time:.4f}s)")
            else:
                print(f"✗")
    
    # Imprimir resultados
    print_results_table(results_dict)
    
    return results_dict


def create_custom_instances(graph_path):
    """Crea instancias personalizadas para prueba."""
    
    print("\n" + "="*100)
    print("CREAR INSTANCIAS PERSONALIZADAS")
    print("="*100)
    
    graph = ColombiaRoadGraph.from_json(graph_path)
    
    # Instancia 1: Andes (Bogotá, Cali, Medellín)
    print("\n📦 Instancia 1: Ruta Andes (3 entregas)")
    deliveries_1 = ["n1037511", "n1110652", "n31567"]  # Bogotá, Cali, Medellín
    print(f"  Entregas: {deliveries_1}")
    
    problem_1 = MultiDeliveryProblem(graph, "n1037511", deliveries_1[1:])
    
    print(f"  → A* (nullHeuristic)...", end=" ", flush=True)
    start = time.perf_counter()
    result_null = aStarSearch(problem_1, heuristic=nullHeuristic)
    time_null = time.perf_counter() - start
    cost_null = problem_1.getCostOfActions(result_null)
    print(f"✓ (costo={cost_null:.2f}km, tiempo={time_null:.4f}s)")
    
    problem_1 = MultiDeliveryProblem(graph, "n1037511", deliveries_1[1:])
    print(f"  → A* (multiDeliveryHeuristic)...", end=" ", flush=True)
    start = time.perf_counter()
    result_multi = aStarSearch(problem_1, heuristic=multiDeliveryHeuristic)
    time_multi = time.perf_counter() - start
    cost_multi = problem_1.getCostOfActions(result_multi)
    print(f"✓ (costo={cost_multi:.2f}km, tiempo={time_multi:.4f}s)")
    
    print(f"  Mejora: {(1-time_multi/time_null)*100:.1f}% más rápido")
    
    # Instancia 2: Caribe (Santa Marta, Cartagena, Sincelejo)
    print("\n📦 Instancia 2: Ruta Caribe (3 entregas)")
    deliveries_2 = ["n1037511", "n11638", "n24949"]  # Bogotá, Cartagena, Sincelejo (aprox)
    print(f"  Entregas: {deliveries_2}")
    
    problem_2 = MultiDeliveryProblem(graph, "n1037511", deliveries_2[1:])
    
    print(f"  → A* (nullHeuristic)...", end=" ", flush=True)
    start = time.perf_counter()
    result_null = aStarSearch(problem_2, heuristic=nullHeuristic)
    time_null = time.perf_counter() - start
    cost_null = problem_2.getCostOfActions(result_null)
    print(f"✓ (costo={cost_null:.2f}km, tiempo={time_null:.4f}s)")
    
    problem_2 = MultiDeliveryProblem(graph, "n1037511", deliveries_2[1:])
    print(f"  → A* (multiDeliveryHeuristic)...", end=" ", flush=True)
    start = time.perf_counter()
    result_multi = aStarSearch(problem_2, heuristic=multiDeliveryHeuristic)
    time_multi = time.perf_counter() - start
    cost_multi = problem_2.getCostOfActions(result_multi)
    print(f"✓ (costo={cost_multi:.2f}km, tiempo={time_multi:.4f}s)")
    
    print(f"  Mejora: {(1-time_multi/time_null)*100:.1f}% más rápido")


if __name__ == '__main__':
    graph_path = "data/colombia_roads.json"
    instances_path = "data/instances.json"
    
    if Path(graph_path).exists() and Path(instances_path).exists():
        results = run_all_experiments(graph_path, instances_path)
        create_custom_instances(graph_path)
    else:
        print("⚠ Falta el archivo de grafo o instancias")
        print(f"  Grafo: {graph_path} - {'✓' if Path(graph_path).exists() else '✗'}")
        print(f"  Instancias: {instances_path} - {'✓' if Path(instances_path).exists() else '✗'}")
