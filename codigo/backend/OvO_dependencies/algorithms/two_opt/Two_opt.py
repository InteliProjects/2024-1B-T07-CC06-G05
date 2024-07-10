def Two_opt_with_greedy(distances, qtd_matrix):
    # Número total de nós no problema
    num_nodes = len(distances)
    # Lista para manter controle dos nós visitados
    visited = [False] * num_nodes
    # Inicia o caminho com o primeiro nó e marca como visitado
    path = [0]
    visited[0] = True
    # Inicializa a distância e o tempo total
    dist = 0
    time = 0

    # Constrói o caminho visitando todos os nós
    for _ in range(1, num_nodes):
        last = path[-1]
        # Encontra o próximo nó com a menor distância não visitado
        next_node = min(
            [(i, dist) for i, dist in enumerate(distances[last]) if not visited[i]],
            key=lambda x: x[1]
        )[0]
        # Atualiza a distância e o tempo total com o custo para o próximo nó
        dist += distances[last][next_node]
        time += distances[last][next_node] / 5 + (2 / 60) * qtd_matrix[last]
        # Marca o próximo nó como visitado e adiciona ao caminho
        visited[next_node] = True
        path.append(next_node)

    # Aplica a otimização 2-opt ao caminho encontrado para melhorar a solução
    path, dist, time = two_opt(path, distances, qtd_matrix)

    # Retorna o caminho final, a distância total e o tempo total
    return {'sequence': path, 'distance': dist, 'time': time}
def two_opt(path, distances, qtd_matrix, max_iterations=100):
    # Flag para controlar se houve melhoria no caminho
    improved = True
    # Contador para controlar o número de iterações
    iteration_count = 0

    # Loop continua enquanto houver melhoria e o número de iterações for menor que o máximo
    while improved and iteration_count < max_iterations:
        improved = False
        # Testa todas as possíveis trocas de segmentos não consecutivos
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if j - i == 1:  # Ignora se i e j são consecutivos
                    continue
                # Verifica se a troca resulta em uma distância menor
                if distances[path[i - 1]][path[i]] + distances[path[j]][path[j + 1]] > distances[path[i - 1]][path[j]] + distances[path[i]][path[j + 1]]:
                    # Realiza a troca invertendo o segmento
                    path[i:j + 1] = path[i:j + 1][::-1]
                    improved = True

        # Incrementa o contador de iterações
        iteration_count += 1

    # Recalcula distância e tempo após a otimização 2-opt
    dist = 0
    time = 0
    for k in range(1, len(path)):
        dist += distances[path[k - 1]][path[k]]
        time += distances[path[k - 1]][path[k]] / 5 + (2 / 60) * qtd_matrix[path[k - 1]]

    # Retorna o caminho otimizado, a distância total e o tempo estimado
    return path, dist, time