package antcolony;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

import static java.nio.charset.StandardCharsets.UTF_8;

/**<b>Responsável pela execução do algoritmo Ant Colony para um cluster de dados da AEGEA (sequenciamento de uma rota)</b><p></p>
 * Propriedades:
 * <ul>
 * <li>ants : int = quantidade de formigas (igual à quantidade de vértices do grafo)
 * <li>iterations : int = quantidade de iterações a serem executadas
 * <li>alpha : int = define o grau de importância dos feromônios para cálculo da probabilidade dos caminhos
 * <li>beta : int = define o grau de importância da distância para cálculo da probabilidade dos caminhos
 * <li>graph : Graph = grafo conexo de hidrômetros
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>Getters</i> e <i>setters</i>
 * <li><i>getSolution</i> : retorna um objeto Route com a rota encontrada
 * <li><i>main</i> : testa execução com arquivo CSV local com nome "dados.csv", contendo dados de um único cluster (uma rota) 
 * </ul>
 */
public class AntColony {
    private final int PROXIMITY_FACTOR = 200;
    private final int PHEROMONE_FACTOR = 100;
    private final double EVAPORATION_COEFFICIENT = 0.70;
    private int ants;
    private int iterations;
    private int alpha;
    private int beta;
    private Graph graph;

    /**
     * @param graph : Graph = grafo de hidrômetros da AEGEA
     * @param iterations : int = iterações do algoritmo
     * @param alpha : int = grau de importância dos feromônios para cálculo da probabilidade dos caminhos
     * @param beta : int = grau de importância dos feromônios para cálculo da probabilidade dos caminhos
     */
    public AntColony(Graph graph, int iterations, int alpha, int beta) {
        this.ants = graph.getVertices();
        this.iterations = iterations;
        this.alpha = alpha;
        this.beta = beta;
        this.graph = graph;
    }

    /**
     * @return rota de hidrômetros sequenciada : Route
     */
    public Route getSolution(int twoOptIterations) {
        boolean[] visited;
        
        for (int i = 0; i < this.iterations; i++) {
            for (int j = 0; j < this.ants; j++) {
                Path[] adjacentPaths = this.graph.getAdjacencyMatrixRow(j);
                this.computeProbabilities(adjacentPaths);

                visited = new boolean[this.ants];
                Path[] path = new Path[this.ants];
                double totalLength = 0;
                Path next = this.getNextPath(adjacentPaths, visited);
                while (next != null) {
                    path[next.getOrigin().getIndex()] = next;
                    totalLength += next.getLength();
                    adjacentPaths = this.graph.getAdjacencyMatrixRow(next.getDestination().getIndex());
                    this.computeProbabilities(adjacentPaths);
                    next = this.getNextPath(adjacentPaths, visited);
                }

                for (Path p : path) {
                    if ( p == null ) { continue; }
                    p.addVisitPheromones(this.PHEROMONE_FACTOR / totalLength);
                }
            }

            Path[][] adjacencyMatrix = this.graph.getAdjacencyMatrix();
            for (int k = 0; k < adjacencyMatrix.length; k++) {
                for (Path p : adjacencyMatrix[k]) {
                    if ( p == null ) { continue; }
                    p.evaporate(this.EVAPORATION_COEFFICIENT);
                    p.spreadPheromones();
                }
            }
        }

        visited = new boolean[this.ants];
        Path[] bestRoute = new Path[this.ants];
        Path[][] adjacencyMatrix = this.graph.getAdjacencyMatrix();
        int nextIndex = 0;
        int count = 0;
        while(count < adjacencyMatrix.length) {
            double highestPheromones = 0;
            int bestPathIndex = 0;
            for (int i = 0; i < adjacencyMatrix.length; i++) {
                Path p = adjacencyMatrix[nextIndex][i];
                if ( p == null ) { continue; }
                if ( p.getPheromones() >= highestPheromones && visited[i] == false) {
                    highestPheromones = p.getPheromones();
                    bestPathIndex = p.getDestination().getIndex();
                }
            }

            visited[nextIndex] = true;
            visited[bestPathIndex] = true;
            adjacencyMatrix[nextIndex][bestPathIndex].getOrigin().setSequence(count);
            bestRoute[count] = adjacencyMatrix[nextIndex][bestPathIndex];
            nextIndex = bestPathIndex;
            count++;
        }

        if (twoOptIterations > 0) {
            return Postprocessing.refineWith2Opt(new Route(bestRoute), twoOptIterations);
        }

        return new Route(bestRoute);
    }

    /**
     * @param paths : Path[] = próximos caminhos possíveis para cálculo de suas respectivas probabilidades de escolha
     */
    private void computeProbabilities(Path[] paths) {
        double[] probs = new double[paths.length];
        double totalProb = 0;
        for (int i = 0; i < paths.length; i++) {
            Path p = paths[i];
            if ( p == null ) { continue; }
            boolean sameStreet = p.getOrigin().getAddress().equals(p.getDestination().getAddress());
            boolean sameSide = p.getOrigin().getAddressNumber() % 2 == p.getDestination().getAddressNumber() % 2;
            double prob = Math.pow(p.getPheromones(), this.alpha) * Math.pow(this.PROXIMITY_FACTOR / p.getLength(), this.beta);
            if ( sameStreet ) { 
                double extra = 1.5D;
                if ( sameSide ) { extra += 1.5D; };
                prob *= extra;
            }
            probs[i] = prob;
            totalProb += prob;
        }

        for (int i = 0; i < paths.length; i++) {
            if ( paths[i] == null ) { continue; }
            paths[i].setProbability(probs[i] / totalProb);
        }
    }

    /**
     * @param paths : Path[] = próximos caminhos possíveis
     * @param visited : boolean[] = índices de hidrômetros já visitados 
     * @return próximo caminho para a formiga visitar : Path
     */
    private Path getNextPath(Path[] paths, boolean[] visited) {
        int nextEdgeIndex = Utils.chooseFromMultinomialDistribution(paths, visited, 100);
        if (nextEdgeIndex == -1) {
            return null;
        }

        visited[paths[nextEdgeIndex].getOrigin().getIndex()] = true;
        visited[paths[nextEdgeIndex].getDestination().getIndex()] = true;
        return paths[nextEdgeIndex];
    }


    public static void main(String[] args) {
        try {
            String fileName;
            int routeCode;
            int iterations;
            int alpha;
            int beta;
            int postIterations = 0;

            if ( args.length < 5 ) {
                System.out.println("Not all necessary arguments were specified.");
                return;
            }
            else {
                fileName = args[0];
                routeCode = Integer.parseInt(args[1]);
                iterations = Integer.parseInt(args[2]);
                alpha = Integer.parseInt(args[3]);
                beta = Integer.parseInt(args[4]);
            }

            if ( args.length >= 6 ) {
                postIterations = Integer.parseInt(args[5]);
            }


            BufferedReader scanner = new BufferedReader(new FileReader(fileName));
            scanner.readLine(); // Discarding headers
            
            ArrayList<Hydrometer> hydrometers = new ArrayList<Hydrometer>();  
            
            String line = scanner.readLine();
            while (line != null) {
                line = new String(line.getBytes(), UTF_8);
                String[] parts = line.split(",");

                double latitude = Double.parseDouble(parts[0]);
                double longitude = Double.parseDouble(parts[1]);  
                String address = parts[2];
                int addressNumber = Integer.parseInt(parts[3]);
                int hAmount = Integer.parseInt(parts[4]);
                hydrometers.add(new Hydrometer(latitude, longitude, address, addressNumber, hAmount, routeCode));

                line = scanner.readLine();
            }

            scanner.close();

            Graph g = new Graph(hydrometers.size());
            for (int i = 0; i < hydrometers.size(); i++) {
                Hydrometer h = hydrometers.get(i);
                for (int j = 0; j < hydrometers.size(); j++) {
                    if (j == i) { continue; }
                    g.addPath(new Path(h, hydrometers.get(j)));
                }
            }

            AntColony antColony = new AntColony(g, iterations, alpha, beta);
            System.out.println(antColony.getSolution(postIterations).toString());

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
