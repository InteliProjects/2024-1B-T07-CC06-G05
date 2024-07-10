package antcolony;


/**<b>Representação de um hidrômetro e sua localização no problema da AEGEA</b><p></p>
 * Propriedades:
 * <ul>
 * <li>latitude : double = coordenada geográfica de latitude
 * <li>longitude : double = coordenada geográfica de longitude
 * <li>index : int = índice na matriz de adjacência
 * <li>sequence : int = indicador da ordem de visita na rota
 * <li>address : String = nome da rua onde está localizado
 * <li>addressNumber : int = número do endereço
 * </ul>
 * 
 * Métodos públicos:<p></p>
 * <ul>
 * <li><i>Getters</i> e <i>setters</i>
 * <li><i>resetIndexCount</i> : reinicia a contagem de índices
 * </ul>
 */
public class Hydrometer {
    private double latitude;
    private double longitude;
    private int index;
    private int sequence;
    private String address;
    private int addressNumber;
    private int hydrometersAmount;
    private int routeCode;
    
    private static int i = 0;
    /**
     * Reinicia a contagem dos índices da matriz de adjacência
     */
    public static void resetIndexCount() {
        i = 0;
    }

     /**
     * @param latitude : double = coordenada geográfica de latitude
     * @param longitude : double = coordenada geográfica de longitude
     * @param address : String = nome da rua do endereço
     * @param addressNumber : int = número do endereço
     * @param hAmount : int = quantidade de hidrômetros presentes neste endereço
     * @param routeCode : int = código da rota a qual esse endereço pertence
     */
    public Hydrometer(double latitude, double longitude, String address, int addressNumber, int hAmount, int routeCode) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.address = address;
        this.addressNumber = addressNumber;
        this.hydrometersAmount = hAmount;
        this.routeCode = routeCode;
        this.index = i;
        i++;
    }

    public double getLatitude() {
        return this.latitude;
    }

    public double getLongitude() {
        return this.longitude;
    }

    public int getIndex() {
        return this.index;
    }

    public int getSequence() {
        return this.sequence;
    }

    public String getAddress() {
        return this.address;   
    }

    public int getAddressNumber() {
        return this.addressNumber;        
    }

    public int getHydrometersAmount() {
        return this.hydrometersAmount;        
    }

    public int getRouteCode() {
        return this.routeCode;        
    }

    public void setSequence(int sequence) {
        this.sequence = sequence;
    }
}