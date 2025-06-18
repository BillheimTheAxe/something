import networkx as nx
import matplotlib.pyplot as plt

# Создание пустого графа
G = nx.Graph()

# Добавление четырёх узлов
nodes = ['A', 'B', 'C', 'D']

# Соединяем первый узел ('A') со всеми остальными узлами
edges = [('A', 'B'), ('A', 'C'), ('A', 'D')]

# Добавляем рёбра в граф
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Визуализация графа (было интересно как нарисуется и решил оставить)
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue')
plt.show()

# Центральность в собственных векторах
centrality = nx.eigenvector_centrality(G)

# Вывод
for node, value in centrality.items():
    print(f"Узел {node}: Центральность {value:.4f}")