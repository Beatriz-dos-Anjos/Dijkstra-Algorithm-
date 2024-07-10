import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
import os
from tkinter import *
from tkinter import messagebox
import numpy as np

def load_graph_data (file,directory): #ler os dados do arquivo database.txt e criar um dataframe
    file_path= os.path.join(directory,file) #construir caminho para arquivo pelo os
    data = pd.read_csv(file_path, header=None, names=['beggining', 'destination', 'distance']) #usar panda para ler o arquivo
    return data

def graph_construc(data): #criar um grafo a partir do df
    graph= nx.Graph() #criar um grafo
    for i in range(len(data)): #percorre cada linha do dataframe 
        graph.add_edge(data['beggining'][i], data['destination'][i], weight=data['distance'][i]) #adiciona arestas ao grafo vazio
    return graph

def dijkstra_algorytm (beggining,destination,Graph): #algoritmo para calcular o caminho com distancia mais curta 
    shortest_path= {} #distancia mais curta
    for node in Graph.nodes():
        shortest_path[node]= math.inf
    shortest_path[beggining]= 0  
    previous={} #o nó anterior no caminho mais curto
    for node in Graph.nodes():
        previous[node]= None

    visited= set() #marcar os nós visitados
    while len(visited)< len(Graph.nodes()):
        current_node= None
        min_path=math.inf
        for node in Graph.nodes():
            if node not in visited and shortest_path[node]<min_path:
                current_node=node
                min_path=shortest_path[node]

        if current_node is None:
            break
        
        visited.add(current_node) #adicionando novo nó à lista de visitados
        
        for neighbor_node, edge_weight in Graph[current_node].items():
            possible_distance=shortest_path[current_node]+edge_weight['weight'] #dist provavel para alcancar o nó vizinho do atual
            if possible_distance<shortest_path[neighbor_node]: #se o possível custo/dist for menor do que o caminho conhecido até o vizinho:
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
        path.reverse() # (fim->inicial) vira (inicial->final), o caminho exibido de forma adequada.
        
        cost_edge=[] #custos das arestas pelo caminho mais curto
        for i in range(len(path)-1): #quantidade de nós no caminho path
            cost_edge.append(Graph[path[i]][path[i+1]]['weight']) #adiciona o custo/peso à lista cost
            
        return path,cost_edge

def update_node_options(): 
    nodes = list(Graph.nodes())
    start_node_menu['menu'].delete(0, 'end')
    end_node_menu['menu'].delete(0, 'end')
    for node in nodes:
        start_node_menu['menu'].add_command(label=node, command=lambda value=node: start_node.set(value))
        end_node_menu['menu'].add_command(label=node, command=lambda value=node: end_node.set(value))

def find_shortest_path():
    beggining = start_node.get()
    destination = end_node.get()
    if beggining and destination:
        result = dijkstra_algorytm(beggining, destination, Graph)
        if isinstance(result, str):
            result_label.config(text=result)
        else:
            path, cost_edge = result
            total_distance = sum(cost_edge)
            result_text = f"Caminho mais curto de {beggining} para {destination}: {path}\nCustos das arestas: {cost_edge}\nDistância Total: {total_distance}"
            result_label.config(text=result_text)
            plot_shortest_path(Graph, path)
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione os nós de início e destino")

def plot_shortest_path(Graph, path):
    plt.figure()
    subgraph = Graph.subgraph(path)
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_color='red', node_size=500, font_size=10, edge_color='red', width=2)
    plt.title('Caminho Mais Curto')
    plt.show()

file='database.txt'
directory='.'
if not os.path.exists(file):
    raise FileNotFoundError(f"O arquivo {file} não foi encontrado no diretório atual.")

data = load_graph_data(file, directory) #ler e carregar os dados
Graph = graph_construc(data) #construir o grafo a partir dos dados

# Criação da janela principal
root = Tk()
root.title("Algoritmo de Dijkstra")
root.configure(bg='#f0f0f0') # fundo cinza claro

# Frame para centralizar os inputs
frame = Frame(root, bg='white', bd=2, relief="groove", padx=20, pady=20)
frame.pack(pady=20, expand=True)

# Canvas para desenhar o círculo vermelho
canvas = Canvas(frame, width=600, height=400, bg='white', highlightthickness=0)
canvas.pack(expand=True)

# Desenhar o círculo vermelho
canvas.create_oval(150, 50, 450, 350, fill='red', outline='')

# Frame para colocar os widgets dentro do círculo
widget_frame = Frame(canvas, bg='red')
canvas.create_window(300, 200, window=widget_frame)

# Configuração das fontes
font_style = ('Arial', 14, 'bold') # fonte mais grossa e legível

# Rótulos e Menus suspensos para selecionar os nós de início e destino
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

# Atualizar opções dos menus com os nós carregados
update_node_options()

# Botão para encontrar o caminho mais curto
find_button = Button(widget_frame, text="Caminho mais curto", command=find_shortest_path, font=font_style, bg='white', fg='black')
find_button.grid(row=2, column=0, columnspan=2, pady=10)

# Rótulo para exibir o resultado
result_label = Label(root, text="", wraplength=400, justify=LEFT, bg='#f0f0f0', fg='black', font=font_style)
result_label.pack(pady=10, expand=True)

# Centralizar a janela na tela
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 3) # Ajuste para centralizar mais para baixo
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Iniciar o loop principal da GUI
root.mainloop()
