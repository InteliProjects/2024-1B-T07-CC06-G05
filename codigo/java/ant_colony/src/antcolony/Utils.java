package antcolony;

import java.util.Random;

/**<b>Contém fórmulas e cálculos matemáticos para utilização em outras estruturas de dados</b><p></p>
 * Propriedades:
 * <ul>
 * <li>WALKING_SPEED : double = constante de velocidade de movimentação de um leiturista da AEGEA em quilômetros por hora
 * <li>READING_SPEED : double = constante de velocidade de leitura de hidrômetro de um leiturista da AEGEA em minutos
 * <li>_random : Random = gerador de valores pseudoaleatórios
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>haversine</i> : fórmula de Haversine para cálculo de distância em quilômetros entre dois pontos expressos por coordenadas geográficas
 * <li><i>chooseFromMultinomialDistribution</i> : escolhe um caminho probabilisticamente através de uma distribuição multinomial
 * <li><i>getWalkingTime</i> : calcula o tempo total de caminhada em horas de um leiturista em relação a uma distância 
 * <li><i>getReadingTime</i> : calcula o tempo total de leitura em horas de um leiturista em relação a um número de hidrômetros 
 * </ul>
 */
public class Utils {
    private static final double WALKING_SPEED = 5;
    private static final double READING_SPEED = 2;
    private static final Random _random = new Random();

    public static double haversine(double originLat, double originLong, double destinationLat, double destinationLong) {
        final int R = 6371; // Radius of the Earth in kilometers 

        originLat = Math.toRadians(originLat);
        originLong = Math.toRadians(originLong);
        destinationLat = Math.toRadians(destinationLat);
        destinationLong = Math.toRadians(destinationLong);

        double deltaLat = destinationLat - originLat;
        double deltaLong = destinationLong - originLong;

        double a = Math.pow(Math.sin(deltaLat / 2), 2) + Math.cos(originLat) * Math.cos(destinationLat) * Math.pow(Math.sin(deltaLong / 2), 2);
        double c = 2 * Math.asin(Math.sqrt(a));
        return c * R;
    }

    public static int chooseFromMultinomialDistribution(Path[] paths, boolean[] excluded, int trials) {
        final int result[] = new int[paths.length];

        for (int i = 0; i < trials; i++) {
            int index = multinomialTrial(paths, excluded);
            if ( index != -1 ) {
                result[index]++;
            }
        }

        int max = 0;
        int maxIndex = -1;
        for (int i = 0; i < result.length; i++) {
            if ( result[i] > max ) {
                max = result[i];
                maxIndex = i;
            }
        }

        return maxIndex;
    }

    private static int multinomialTrial(Path[] paths, boolean[] excluded) {
        double sample = _random.nextDouble();
        for (int i = 0; i < paths.length; ++i) {
            if (paths[i] == null) { continue; }
            if (sample < paths[i].getProbability() && excluded[i] == false) {
                return i;
            }
        }
        return -1;
    }

    public static double getWalkingTime(double distance) {
        return distance / WALKING_SPEED;
    }

    public static double getReadingTime(int hydrometers) {
        return hydrometers * READING_SPEED / 60;
    }

    public static double manhattan(double originLat, double originLong, double destinationLat, double destinationLong) {
        return Math.abs(originLat - destinationLat) + Math.abs(originLong - destinationLong);
    }
}
