"""
Este módulo implementa o Algoritmo de Polinização por Flores (FPA) para resolver problemas de otimização,
usando estratégias de polinização biótica e abiótica.

Classes:
    FPA: Uma classe que representa o Algoritmo de Polinização por Flores com métodos para realizar
         polinização biótica e abiótica, inicializar soluções, calcular distâncias e executar o loop principal.

Exemplo de uso:
    dist_matrix = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
    switch_prob = 0.8
    number_nodes = 3
    number_flowers = 10

    fpa = FPA(dist_matrix, switch_prob, number_nodes, number_flowers)
    best_distance, best_solution = fpa.main_loop()
    print(f"Melhor distância: {best_distance}")
    print(f"Melhor solução: {best_solution}")
"""

import numpy as np
from scipy.stats import levy
import random

class FPA:
    """
    Implementação do Algoritmo de Polinização por Flores (FPA).
    
    Atributos:
        n (int): Número de nós.
        m (int): Número de flores.
        D_matrix (np.ndarray): Matriz de distâncias.
        s_prob (float): Probabilidade de troca.
    """

    def __init__(self, dist_matrix, switch_prob, number_nodes, number_flowers):
        """
        Inicializa o FPA com os parâmetros fornecidos.

        Args:
            dist_matrix (list de listas de float): Matriz de distâncias.
            switch_prob (float): Probabilidade de troca.
            number_nodes (int): Número de nós.
            number_flowers (int): Número de flores.
        """
        self.n = number_nodes
        self.m = number_flowers
        self.D_matrix = np.array(dist_matrix, dtype=np.float64)
        self.s_prob = switch_prob

    def biotic_pollination(self, costs):
        """
        Realiza a polinização biótica usando uma distribuição de voo de Levy.

        Args:
            costs (list de tuplas): Lista de tuplas onde cada tupla contém o custo e o nó correspondente.

        Returns:
            int: O nó selecionado com base na polinização biótica.
        """
        costs_array = np.array(costs)
        probs = []
        r = random.random()
        for i in range(len(costs)):
            lev = levy.cdf(np.sum(costs_array[:i+1, 0], axis=0)) - levy.cdf(np.sum(costs_array[:i, 0], axis=0))
            probs.append((lev, costs_array[i][1]))
        min_val = float('inf')
        min_node = None
        for i in probs:
            if abs(i[0] - r) < min_val:
                min_node = i
                min_val = abs(i[0] - r)
        return min_node

    def abiotic_pollination(self, costs, radius, previous_node):
        """
        Realiza a polinização abiótica com base em restrições de distância.

        Args:
            costs (list de tuplas): Lista de tuplas onde cada tupla contém o custo e o nó correspondente.
            radius (float): Raio dentro do qual a polinização abiótica pode ocorrer.
            previous_node (int): O nó anterior.

        Returns:
            list: Uma lista contendo um booleano indicando sucesso e o nó selecionado.
        """
        new_costs = []
        for i in costs:
            if self.D_matrix[int(previous_node)][int(i[1])] <= radius:
                new_costs.append(i)
        if len(new_costs) == 0:
            return [False, None]
        probs = []
        costs_array = np.array(new_costs)
        r = random.random()
        for i in range(len(new_costs)):
            categorical = np.sum(costs_array[:i+1, 0])
            probs.append((categorical, costs_array[i][1]))
        min_val = float('inf')
        min_node = None
        for i in probs:
            if abs(i[0] - r) <= min_val:
                min_node = i
                min_val = abs(i[0] - r)
        return [True, min_node]

    def initialize_solutions(self):
        # """
        # Inicializa as soluções aleatoriamente.

        # Returns:
        #     list: Uma lista de soluções inicializadas.
        # """
        # sol = []
        # for i in range(self.m):
        #     sol.append(random.sample(range(self.n), self.n))
        # return sol
        """
        Inicializa as soluções aleatoriamente.

        Returns:
            list: Uma lista de soluções inicializadas.
        """
        sol = []
        for i in range(self.m):
            sol.append([])
            for j in range(self.n):
                if j == 0:
                    random_init = random.randint(0, self.n - 1)
                    sol[i].append(random_init)
                else:
                    sol[i].append(0)
        return sol

    def calculate_distance(self, solution):
        """
        Calcula a distância total de uma solução dada.

        Args:
            solution (list): Uma lista representando o caminho da solução.

        Returns:
            float: A distância total da solução.
        """
        distance = 0
        for i in range(1, self.n):
            distance += self.D_matrix[int(solution[i-1]), int(solution[i])]
        return distance

    def calculate_cost(self, vertices, node, cost_map):
        """
        Calcula os custos para cada vértice a partir de um nó dado.

        Args:
            vertices (list): Lista de vértices.
            node (int): O nó atual.
            cost_map (np.ndarray): Mapa de custos baseado na matriz de distâncias.

        Returns:
            list: Lista de tuplas onde cada tupla contém o custo normalizado e o vértice correspondente.
        """
        current_costs = [(cost_map[int(node)][int(vertice)], vertice) for vertice in vertices]
        A = sum(cost[0] for cost in current_costs)
        for i in range(len(current_costs)):
            if A == 0:
                current_costs[i] = (0, current_costs[i][1])
            else:
                current_costs[i] = (current_costs[i][0] / A, current_costs[i][1])
        current_costs.sort(key=lambda x: x[1], reverse=True)
        print(current_costs)
        return current_costs

    def main_loop(self,qtd_matrix,radius):
        """
        Executa o loop principal do FPA.

        Returns:
            dict: Um dicionário contendo a melhor sequência, a melhor distância e o tempo.
        """
        cost_map = 1 / self.D_matrix
        cost_map[np.isinf(cost_map)] = 0
        solution = self.initialize_solutions()
        for i in range(self.m):
            vertices = [k for k in range(0, self.n) if k != solution[i][0]]
            for j in range(1, self.n):
                previous_node = solution[i][j-1]
                costs = self.calculate_cost(vertices, previous_node, cost_map)
                r = random.random()
                if r >= self.s_prob:
                    current_node = self.biotic_pollination(costs)
                else:
                    success, current_node = self.abiotic_pollination(costs, radius, previous_node)
                    if not success:
                        current_node = self.biotic_pollination(costs)
                solution[i][j] = current_node[1]
                vertices.remove(int(current_node[1]))
        distances = [(self.calculate_distance(s), s) for s in solution]
        distances.sort(key=lambda x: x[0])
        best_distance, best_solution = distances[0]
        best_solution = [int(i) for i in best_solution]
        time=0
        for i in qtd_matrix:
            time += i*(0.5/60)
        time+= best_distance/5
        return {'sequence': best_solution, 'distance': best_distance, 'time': time}