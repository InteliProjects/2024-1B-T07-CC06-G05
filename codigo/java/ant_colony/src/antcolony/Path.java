package antcolony;
/**<b>Representação de um caminho entre dois hidrômetros no problema da AEGEA modelado para execução do algoritmo Ant Colony</b><p></p>
 * Propriedades:
 * <ul>
 * <li>origin : Hydrometer = hidrômetro de origem
 * <li>destination : Hydrometer = hidrômetro de destino
 * <li>pheromones : double = feromônios deixados pelas formigas na execução do algoritmo a cada iteração
 * <li>visitPheromones : double = contagem dos feromônios deixados a cada visita de formigas
 * <li>length : double = extensão do caminho em quilômetros
 * <li>probability : double = probabilidade de escolha do caminho para as formigas
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>Getters</i> e <i>setters</i>
 * <li><i>addVisitPheromones</i> : adiciona feromônios a cada visita de formigas
 * <li><i>evaporate</i> : evapora feromônios a cada iteração do algoritmo
 * <li><i>spreadPheromones</i> : "espalha" feromônios a cada iteração do algoritmo, ou seja, adiciona os de visita aos de iteração
 * </ul>
 */
public class Path {
    private Hydrometer origin;
    private Hydrometer destination;
    private double pheromones;
    private double visitPheromones;
    private double length;
    private double probability;

    /**
     * @param origin : Hydrometer = hidrômetro de origem
     * @param destination : Hydrometer = hidrômetro de destino
     */
    public Path(Hydrometer origin, Hydrometer destination) {
        this.origin = origin;
        this.destination = destination;
        this.pheromones = 1;
        this.visitPheromones = 0;
        this.length = Utils.haversine(origin.getLatitude(), origin.getLongitude(), destination.getLatitude(), destination.getLongitude());
        this.probability = 0;
    }

    public Hydrometer getOrigin() {
        return this.origin;
    }

    public Hydrometer getDestination() {
        return this.destination;
    }

    public double getPheromones() {
        return this.pheromones;
    }
    
    public double getvisitPheromones() {
        return this.visitPheromones;
    }

    public double getLength() {
        return this.length;
    }

    public double getProbability() {
        return this.probability;
    }


    public void setPheromones(double pheromones) {
        this.pheromones = pheromones;
    }

    public void setProbability(double probability) {
        this.probability = probability;
    }

    /**
     * @param visitPheromones : double = feromônios a serem adicionados na atual visita
     */
    public void addVisitPheromones(double visitPheromones) {
        this.visitPheromones += visitPheromones;
    }

    /**
     * @param evaporationFactor : double = porcentagem que sobrará dos feromônios após evaporação
     */
    public void evaporate(double evaporationFactor) {
        this.pheromones *= evaporationFactor;
    }

    /**
     * Adiciona os feromônios de visita aos de iteração e reinicia o valor dos feromônios de visita
     */
    public void spreadPheromones() {
        this.pheromones += this.visitPheromones;
        this.visitPheromones = 0;
    }
}
