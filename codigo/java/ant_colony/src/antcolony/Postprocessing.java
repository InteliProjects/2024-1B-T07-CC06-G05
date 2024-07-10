package antcolony;

/**<b>Responsável pelo refinamento do resultado do algoritmo Ant Colony para um cluster de dados da AEGEA (sequenciamento de uma rota)</b><p></p>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>refineWith2Opt</i> : retorna um objeto Route com a rota refinada pelo algoritmo 2-Opt
 * </ul>
 */
public class Postprocessing {
    
    /**
     * 
     * @param r : Route = rota a ser refinada pelo algoritmo 2-Opt
     * @param maxIterations : int = máximo de iterações do 2-Opt
     * 
     * @return rota de hidrômetros sequenciada refinada : Route
     */
    public static Route refineWith2Opt(Route r, int maxIterations) {
        boolean improved = true;
        int iteration = 0;
        Hydrometer[] sortedHydrometers = r.getHydrometers();

        while ( improved && iteration <= maxIterations ) {
            improved = false;

            for (int i = 1; i < sortedHydrometers.length - 1; i++) {
                for (int j = i + 1; j < sortedHydrometers.length; j++) {
                    Hydrometer h1 = sortedHydrometers[i - 1];
                    Hydrometer h2 = sortedHydrometers[i];
                    Hydrometer h3 = sortedHydrometers[j];
                    if (!h1.getAddress().equals(h3.getAddress())) { continue; }

                    double dist = Utils.manhattan( h1.getLatitude(), h1.getLongitude(), h2.getLatitude(), h2.getLongitude() );
                    if ( dist > Utils.manhattan(h1.getLatitude(), h1.getLongitude(), h3.getLatitude(), h3.getLongitude()) );
                        int sequence = h3.getSequence();
                        h3.setSequence(h2.getSequence());
                        h2.setSequence(sequence);
                        sortedHydrometers[i] = h3;
                        sortedHydrometers[j] = h2;
                        improved = true;
                }
            }

            iteration++;
        }

        double newLength = 0;
        double newTravelTime = 0;
        for (int i = 1; i < sortedHydrometers.length; i++) {
            Hydrometer h1 = sortedHydrometers[i - 1];
            Hydrometer h2 = sortedHydrometers[i];
            double dist = Utils.haversine( h1.getLatitude(), h1.getLongitude(), h2.getLatitude(), h2.getLongitude() );

            newTravelTime += Utils.getWalkingTime(dist) + Utils.getReadingTime(h1.getHydrometersAmount());
            newLength += dist;
        }
        newTravelTime += Utils.getReadingTime(sortedHydrometers[sortedHydrometers.length - 1].getHydrometersAmount());

        r.setHydrometers(sortedHydrometers);
        r.setTravelTime(newTravelTime);
        r.setLength(newLength);
        return r;
    }
}
