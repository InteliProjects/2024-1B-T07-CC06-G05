package antcolony;

/**<b>Representação de uma rota de visitação no problema da AEGEA</b><p></p>
 * Propriedades:
 * <ul>
 * <li>hydrometers : Hydrometer[] = <i>array</i> de hidrômetros contidos na rota
 * <li>travelTime : double = tempo total de travessia da rota em horas
 * <li>length : double = extensão da rota em quilômetros
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>Getters</i> e <i>setters</i>
 * <li><i>toString (override)</i> : permite a visualização da rota no console como uma string
 * </ul>
 */
public class Route {
    private Hydrometer[] hydrometers;
    private double travelTime;
    private double length;

    /**
     * @param paths : Path[] = caminhos incluídos na rota
     */
    public Route(Path[] paths) {
        this.hydrometers = new Hydrometer[paths.length];
        this.travelTime = 0;
        this.length = 0;

        for (Path p : paths) {
            this.length += p.getLength();
            this.travelTime += Utils.getWalkingTime(p.getLength());
            this.hydrometers[p.getOrigin().getSequence()] = p.getOrigin();
            this.travelTime += Utils.getReadingTime(p.getOrigin().getHydrometersAmount());
        }
    }

    /**
     * @return array de hidrômetros da rota : Hydrometer[]
     */
    public Hydrometer[] getHydrometers() {
        return this.hydrometers;
    }

    /**
     * @return tempo de viagem da rota em horas : double
     */
    public double getTravelTime() {
        return this.travelTime;
    }

    /**
     * @return extensão da rota em km : double
     */
    public double getLength() {
        return this.length;
    }

    /**
     * @param hydrometers : Hydrometer[] = array de hidrômetros da rota
     */
    public void setHydrometers(Hydrometer[] hydrometers) {
        this.hydrometers = hydrometers;
    }

    /**
     * @param travelTime : double = tempo de viagem da rota em horas
     */
    public void setTravelTime(double travelTime) {
        this.travelTime = travelTime;
    }

    /**
     * @param length : double = extensão da rota em km
     */
    public void setLength(double length) {
        this.length = length;
    }

    /**
     * Sobrescrição do método de conversão para String para testes e depuração.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("\n\"Rota ");
        sb.append(this.hydrometers[0].getRouteCode());
        sb.append("\": {\n\"Tempo\": \"");
        sb.append(this.travelTime);
        sb.append("h\"");
        sb.append(",\n\"Tamanho\": \"");
        sb.append(this.length);
        sb.append("km\",\n\"Pontos\": [");

        for (Hydrometer h : hydrometers) { 
            sb.append("\n{\n\"LOGRADOURO\": \"");
            sb.append(h.getAddress());
            sb.append("\",\n\"NUMERO\": ");
            sb.append(h.getAddressNumber());
            sb.append(",\n\"SEQUENCIA\": ");
            sb.append(h.getSequence());
            sb.append(",\n\"LATITUDE\": ");
            sb.append(h.getLatitude());
            sb.append(",\n\"LONGITUDE\": ");
            sb.append(h.getLongitude());
            sb.append("\n},");
        }

        sb.deleteCharAt(sb.length()-1);
        sb.append("\n]\n},");
        return sb.toString();
    }
}
