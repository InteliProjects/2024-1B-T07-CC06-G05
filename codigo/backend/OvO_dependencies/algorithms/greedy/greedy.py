def greedy_tsp(distances,qtd_matrix):
    num_nodes = len(distances)
    visited = [False] * num_nodes
    path = [0]
    visited[0] = True
    dist =0
    time = 0

    for _ in range(1, num_nodes):
        last = path[-1]
        next_node = min(
            [(i, dist) for i, dist in enumerate(distances[last]) if not visited[i]],
            key=lambda x: x[1]
        )[0]
        dist+= distances[last][next_node]
        time += distances[last][next_node]/5 +(2/60)*qtd_matrix[last]

        visited[next_node] = True
        path.append(next_node)
   
    return {'sequence':path,'distance':dist,'time':time}