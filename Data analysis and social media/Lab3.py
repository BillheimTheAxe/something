import networkx as nx
import random
random.seed(42)  # Фиксируем генератор случайных чисел для воспроизводимости

# Данные
n = 15           # Вершины
p = 0.85         # Вероятность появления ребра

# Генерация графа по модели Эрдёша-Реньи
G = nx.erdos_renyi_graph(n, p)

# Список степеней вершин
degrees = list(dict(nx.degree(G)).values())

# Вычисление реальной средней степени
average_degree_practical = sum(degrees) / len(degrees)

# Аналитическая средняя степень
expected_average_degree = (n - 1) * p

# Вывод
print(f"Средняя степень (реальная): {average_degree_practical:.2f}")
print(f"Средняя степень (теоретическая): {expected_average_degree:.2f}")