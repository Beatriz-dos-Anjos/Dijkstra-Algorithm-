import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
import os
from tkinter import *
from tkinter import messagebox
import numpy as np

def load_graph_data(file, directory):  #caminho para o arquivo
    file_path = os.path.join(directory, file) 
    data = pd.read_csv(file_path, header=None, names=['beginning', 'destination', 'distance'])
    return data

def graph_construct(data):
    graph = {}  
    for i in range(len(data)): #iterando pelo banco de dados, extrai os valores das 3 colunas para a linha
        beginning=data['beginning'][i] #1
        destination=data['destination'][i] #2
        distance =  data['distance'][i] #3
        #presença do nó de origem e destino - caso negativa, adiciona ao grafo
        if beginning not in graph:
            graph[beginning] = {}
        if destination not in graph:
            graph[destination] = {}
        
        graph[beginning][destination] = distance
        graph[destination][beginning] = distance
    
    return graph

def dijkstra_algorithm(beginning, destination, graph):
    shortest_path = {}  #distância mais curta
    for node in graph:
        shortest_path[node] = math.inf    
    shortest_path[beginning] = 0  
    previous = {} #o nó anterior no caminho mais curto
    for node in graph:
        previous[node] = None
    visited = set() #marcar os nós visitados
    while len(visited) < len(graph):
        current_node = None
        min_path = math.inf
        for node in graph:
            if node not in visited and shortest_path[node] < min_path:
                current_node = node
                min_path = shortest_path[node]

        if current_node is None:
            break
        
        visited.add(current_node) #adicionando novo nó à lista de visitados
        
        for neighbor_node, edge_weight in graph[current_node].items():
            possible_distance = shortest_path[current_node] + edge_weight  #dist provavel para alcancar o nó vizinho do atual
            if possible_distance < shortest_path[neighbor_node]:  # se o possível custo/dist for menor do que o caminho conhecido até o vizinho:
                shortest_path[neighbor_node] = possible_distance #atualização da distância menor
                previous[neighbor_node] = current_node  #atualização das anteriores
    
    if shortest_path[destination] == math.inf:
        return "Não existe caminho entre os nós"
    else:
        path = []
        node = destination
        while node is not None:  #alcancando nós:
            path.append(node) #adiciona à lista path ( fim ->inicio)
            node = previous[node] #para retroceder, o nó atual é atualizado para ser seu predecessor.
        path.reverse() # (fim->inicial) vira  (inicial->final) , o caminho exibido de forma adequada.
        
        cost_edge = [graph[path[i]][path[i + 1]] for i in range(len(path) - 1)]  #adiciona o custo/peso à lista cost
            
        
        return path, cost_edge

def update_node_options():
    nodes = list(Graph.keys())
    start_node_menu['menu'].delete(0, 'end')
    end_node_menu['menu'].delete(0, 'end')
    for node in nodes:
        start_node_menu['menu'].add_command(label=node, command=lambda value=node: start_node.set(value))
        end_node_menu['menu'].add_command(label=node, command=lambda value=node: end_node.set(value))

def find_shortest_path():
    beginning = start_node.get()
    destination = end_node.get()
    if beginning and destination:
        result = dijkstra_algorithm(beginning, destination, Graph)
        if isinstance(result, str):
            result_label.config(text=result)
        else:
            path, cost_edge = result
            cost_edge = [float(cost) for cost in cost_edge]
            total_distance = sum(cost_edge)
            result_text = (
                f"Caminho mais curto de {beginning} para {destination}: {' -> '.join(path)}\n"
                f"Custos das arestas: {', '.join(map(str, cost_edge))}\n"
                f"Distância Total: {total_distance:.2f}"
            )
            result_label.config(text=result_text)
            plot_shortest_path(Graph, path)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione os nós de origem e destino")

def plot_shortest_path(graph, path):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
            
    pos = nx.spring_layout(G) # Utiliza o layout spring para melhor organização dos nós
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, edge_color='gray', width=2, font_weight='bold')
    
    path_edges = list(zip(path, path[1:]))    # Destaque o caminho mais curto em vermelho
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    
    plt.show()

file = 'database.txt'
directory = '.'

data = load_graph_data(file, directory)
Graph = graph_construct(data)

root = Tk()
root.title("Algoritmo de Dijkstra")
root.configure(bg='#f0f0f0')

frame = Frame(root, bg='white', bd=2, relief="groove", padx=20, pady=20)
frame.pack(pady=20, expand=True)

canvas = Canvas(frame, width=600, height=400, bg='white', highlightthickness=0)
canvas.pack(expand=True)
canvas.create_oval(150, 50, 450, 350, fill='red', outline='')

widget_frame = Frame(canvas, bg='red')
canvas.create_window(300, 200, window=widget_frame)

font_style = ('Arial', 14, 'bold')

Label(widget_frame, text="ORIGEM:", bg='red', fg='white', font=font_style).grid(row=0, column=0, padx=10, pady=5)
start_node = StringVar(root)
start_node_menu = OptionMenu(widget_frame, start_node, "")
start_node_menu.config(font=font_style)
start_node_menu.grid(row=0, column=1, padx=10, pady=5)

Label(widget_frame, text="DESTINO:", bg='red', fg='white', font=font_style).grid(row=1, column=0, padx=10, pady=5)
end_node = StringVar(root)
end_node_menu = OptionMenu(widget_frame, end_node, "")
end_node_menu.config(font=font_style)
end_node_menu.grid(row=1, column=1, padx=10, pady=5)

update_node_options()

find_button = Button(widget_frame, text="Caminho", command=find_shortest_path, font=font_style, bg='white', fg='black')
find_button.grid(row=2, column=0, columnspan=2, pady=10)

result_label = Label(root, text="", wraplength=400, justify=LEFT, bg='#f0f0f0', fg='black', font=font_style)
result_label.pack(pady=10, expand=True)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 3) - (height // 3)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.mainloop()
