package antcolony;

/**<b>Representação de um grafo onde os vértices são os hidrômetros no problema da AEGEA e as arestas são os caminhos entre os mesmos</b><p></p>
 * Propriedades:
 * <ul>
 * <li>vertices : int = quantidade de hidrômetros ou vértices
 * <li>adjacencyMatrix : Path[][] = matriz de adjacência de hidrômetros ou vértices
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>Getters</i> e <i>setters</i>
 * <li><i>getAdjacencyMatrixRow</i> : retorna apenas uma linha da matriz de adjacência
 * <li><i>addPath</i> : adiciona um caminho à matriz de adjacência
 * </ul>
 */
public class Graph {
    private int vertices;
    private Path[][] adjacencyMatrix;

    public Graph(int vertices) {
        this.vertices = vertices;
        this.adjacencyMatrix = new Path[this.vertices][this.vertices];
    }

    public int getVertices() {
        return this.vertices;
    }

    public Path[][] getAdjacencyMatrix() {
        return this.adjacencyMatrix;
    }

    /**
     * @param index : int = índice da linha na matriz de adjacência
     * @return caminhos contidos na linha especificada : Path[]
     */
    public Path[] getAdjacencyMatrixRow(int index) {
        return this.adjacencyMatrix[index];
    }
    
    /**
     * @param p : Path = caminho a ser adicionado na matriz de adjacência
     */
    public void addPath(Path p) {
        this.adjacencyMatrix[p.getOrigin().getIndex()][p.getDestination().getIndex()] = p;
    }
}
