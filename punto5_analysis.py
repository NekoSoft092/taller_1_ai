#!/usr/bin/env python3
"""Análisis Punto 5: Comparación de heurísticas en MultiDelivery."""

import json
import time
from pathlib import Path
from algorithms.search import aStarSearch
from algorithms.heuristics import (
    straightLineMultiDeliveryHeuristic,
    multiDeliveryHeuristic,
)
from algorithms.problems import MultiDeliveryProblem, actions_to_route
from graph.road_graph import ColombiaRoadGraph


def run_analysis():
    """Ejecuta análisis de Punto 5."""
    
    # Cargar datos
    graph = ColombiaRoadGraph.from_json("data/colombia_roads.json")
    with open("data/instances.json") as f:
        instances_data = json.load(f)
    
    # Casos multidelivery
    multi_cases = {
        "multi_andes_caribe": instances_data["multi_andes_caribe"],
        "multi_national_challenge": instances_data["multi_national_challenge"],
    }
    
    print("\n" + "="*100)
    print("PUNTO 5: ANÁLISIS DE ENTREGAS MÚLTIPLES (A* CON DIFERENTES HEURÍSTICAS)")
    print("="*100)
    
    results = {}
    
    for case_name, config in multi_cases.items():
        print(f"\n{case_name.upper()}")
        print("-" * 100)
        
        start = config["start"]
        deliveries = config["deliveries"]
        num_deliveries = len(deliveries)
        
        print(f"Nodo inicio: {start}")
        print(f"Entregas ({num_deliveries}): {deliveries}\n")
        
        results[case_name] = {}
        
        # Test 1: straightLineMultiDeliveryHeuristic (distancias geodésicas)
        print("1️⃣  A* con straightLineMultiDeliveryHeuristic (distancias geodésicas)")
        print("   " + "─" * 90)
        
        problem1 = MultiDeliveryProblem(graph, start, deliveries)
        start_time = time.perf_counter()
        actions1 = aStarSearch(problem1, heuristic=straightLineMultiDeliveryHeuristic)
        time1 = time.perf_counter() - start_time
        
        cost1 = problem1.getCostOfActions(actions1) if actions1 else None
        expanded1 = problem1._expanded
        frontier1 = problem1._max_frontier_size
        
        print(f"   ✓ Costo (km):        {cost1:.2f}")
        print(f"   ✓ Tramos:            {len(actions1) if actions1 else 0}")
        print(f"   ✓ Nodos expandidos:  {expanded1}")
        print(f"   ✓ Frontera máx:      {frontier1}")
        print(f"   ✓ Tiempo (s):        {time1:.3f}\n")
        
        results[case_name]["straightLine"] = {
            "cost": cost1,
            "actions": len(actions1) if actions1 else 0,
            "expanded": expanded1,
            "frontier": frontier1,
            "time": time1,
        }
        
        # Test 2: multiDeliveryHeuristic (distancias reales + MST)
        print("2️⃣  A* con multiDeliveryHeuristic (distancias reales + MST)")
        print("   " + "─" * 90)
        
        problem2 = MultiDeliveryProblem(graph, start, deliveries)
        start_time = time.perf_counter()
        actions2 = aStarSearch(problem2, heuristic=multiDeliveryHeuristic)
        time2 = time.perf_counter() - start_time
        
        cost2 = problem2.getCostOfActions(actions2) if actions2 else None
        expanded2 = problem2._expanded
        frontier2 = problem2._max_frontier_size
        
        print(f"   ✓ Costo (km):        {cost2:.2f}")
        print(f"   ✓ Tramos:            {len(actions2) if actions2 else 0}")
        print(f"   ✓ Nodos expandidos:  {expanded2}")
        print(f"   ✓ Frontera máx:      {frontier2}")
        print(f"   ✓ Tiempo (s):        {time2:.3f}\n")
        
        results[case_name]["multiDelivery"] = {
            "cost": cost2,
            "actions": len(actions2) if actions2 else 0,
            "expanded": expanded2,
            "frontier": frontier2,
            "time": time2,
        }
        
        # Comparación
        print("📊 COMPARACIÓN")
        print("   " + "─" * 90)
        
        if expanded1 is not None and expanded2 is not None:
            reduction = (1 - expanded2 / expanded1) * 100
            print(f"   Reducción nodos expandidos: {reduction:+.1f}%")
            print(f"   ({expanded1} → {expanded2} nodos)")
        
        if time1 is not None and time2 is not None:
            time_ratio = time2 / time1
            print(f"   Ratio de tiempo: {time_ratio:.2f}x")
        
        if cost1 == cost2:
            print(f"   ✓ Ambas heurísticas encuentran la misma solución óptima: {cost1:.2f} km")
        else:
            print(f"   ⚠ Soluciones diferentes: {cost1:.2f} vs {cost2:.2f} km")
    
    # Tabla resumen
    print("\n" + "="*100)
    print("TABLA RESUMEN - PUNTO 5")
    print("="*100)
    
    print("\n| Caso | Heurística | Costo (km) | Tramos | Expandidos | Frontera | Tiempo (s) |")
    print("|------|------------|-----------|--------|-----------|----------|-----------|")
    
    for case_name in ["multi_andes_caribe", "multi_national_challenge"]:
        if case_name in results:
            r = results[case_name]
            
            # straightLineMultiDeliveryHeuristic
            s = r["straightLine"]
            print(f"| {case_name} | straightLine | {s['cost']:.2f} | {s['actions']} | {s['expanded']} | {s['frontier']} | {s['time']:.3f} |")
            
            # multiDeliveryHeuristic
            m = r["multiDelivery"]
            print(f"| {case_name} | multiDelivery | {m['cost']:.2f} | {m['actions']} | {m['expanded']} | {m['frontier']} | {m['time']:.3f} |")
    
    print("\n" + "="*100)


if __name__ == "__main__":
    run_analysis()
