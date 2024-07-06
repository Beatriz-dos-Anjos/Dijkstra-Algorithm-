import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
from tkinter import * 
import numpy as np
import math


def dijkstra_algorytm (beggining,destination,Graph):
    shortest_path= {}  #distancia mais curta
    for node in Graph.nodes():
        shortest_path[node]= math.inf
    shortest_path[beggining]= 0  
    previous={}  #o nó anterior no caminho mais curto
    for node in Graph.nodes():
        previous[node]= None

    visited= set()    #marcar os nós visitados
    while len(visited)< len(Graph.nodes()):
        current_node= None
        min_path=math.inf
        for node in Graph.nodes():
            if node not in visited and shortest_path[node]<min_path:
                current_node=node
                min_path=shortest_path[node]

        visited.add(current_node) #adicionando novo nó à lista de visitados
        
        if current_node is None:
            break
        
        for neighbor_node, edge_weight in Graph[current_node].items():
            possible_distance=shortest_path[current_node]+edge_weight['distance'] #dist provavel para alcancar o nó vizinho do atual
            if possible_distance<shortest_path[neighbor_node]: # se o possível custo/dist for menor do que o caminho conhecido até o vizinho:
                shortest_path[neighbor_node]=possible_distance #atualização da distância menor
                previous[neighbor_node]=current_node #atualização dos anteriores. 
    
    if shortest_path[destination]==math.inf:
        return "Não existe caminho entre os nós"
    else:
        path= []
        node= destination #nó almejado que irá voltar para o caminho curto.
        while node is not None: #alcancando nós:
            path.append(node) #adiciona à lista path ( fim ->inicio)
            node=previous[node] #para retroceder, o nó atual é atualizado para ser seu predecessor.
        path.reverse() # (fim->inicial) vira  (inicial->final) , o caminho exibido de forma adequada.
        
        cost_edge=[]   #custos das arestas pelo caminho mais curto
        for i in range(len(path)-1): #quantidade de nós no caminho path
            cost_edge.append(Graph[path[i]][path[i+1]]['distance']) #adiciona o custo/peso à lista cost
            
        return path,cost_edge
        

