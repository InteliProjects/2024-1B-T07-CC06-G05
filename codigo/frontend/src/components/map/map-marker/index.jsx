import styles from "./style.module.css";

/**
 * Componente de marcador de mapa.
 *
 * @component
 * @param {Object} props - As propriedades do componente.
 * @param {string} props.label - O rótulo do marcador.
 * @param {function} props.onClick - O manipulador de evento de clique no marcador.
 * @param {number} props.zoom - O nível de zoom do mapa.
 * @param {number} props.lat - A latitude do marcador.
 * @param {number} props.lng - A longitude do marcador.
 * @returns {JSX.Element} O elemento JSX do marcador de mapa.
 */
const MapMarker = ({ label, zoom, onClick }) => (
  <div
    className={styles.marker}
    onClick={onClick}
    style={{
      transform: `translate(-50%, -50%) scale(${zoom / 22 ** 1.1})`,
    }}
  >
    {label && <span className={styles.label}>{label}</span>}
  </div>
);

export default MapMarker;
