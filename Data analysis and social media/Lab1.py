import heapq  # используем очередь с приоритетом для эффективного выбора минимальной вершины


def dijkstra(graph, start):
    n = len(graph)

    # Изначально считаем расстояния до всех вершин бесконечностью
    distances = {v: float('inf') for v in range(n)}
    distances[start] = 0  # Расстояние до самого себя равно нулю

    # Используем кучу для хранения вершин, отсортированных по расстоянию
    priority_queue = [(0, start)]  # Куча пар (расстояние, вершина)

    while priority_queue:
        current_distance, u = heapq.heappop(priority_queue)

        if current_distance > distances[u]:
            continue  # Пропускаем вершины, если новое расстояние больше текущего

        # Обходим всех соседей вершины u
        for v in range(n):
            weight = graph[u][v]
            if weight != 0:  # Проверяем наличие ребра
                distance = current_distance + weight

                # Если нашли более короткий путь до соседней вершины
                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(priority_queue, (distance, v))

    return distances


# Пример использования
if __name__ == "__main__":
    # Матрица смежности (граф ненаправленный и взвешенный)
    graph = [
        [0, 7, 9, 0, 0, 14],
        [7, 0, 10, 15, 0, 0],
        [9, 10, 0, 11, 0, 2],
        [0, 15, 11, 0, 6, 0],
        [0, 0, 0, 6, 0, 9],
        [14, 0, 2, 0, 9, 0]
    ]

    start_vertex = 0  # Стартовая вершина
    shortest_paths = dijkstra(graph, start_vertex)

    print("Кратчайшие пути от вершины {}: {}".format(start_vertex, shortest_paths))