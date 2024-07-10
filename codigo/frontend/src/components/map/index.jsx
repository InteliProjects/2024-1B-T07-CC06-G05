import GoogleMapReact from "google-map-react";
import { useState } from "react";
import MapMarker from "./map-marker";
import { useEffect } from "react";
import calculateCenterPoint from "../../utils/calculate-center-point";

/**
 * Componente de mapa.
 *
 * @param {object} props - As propriedades do componente.
 * @param {Array} props.route - A rota a ser exibida no mapa.
 * @returns {JSX.Element} O elemento JSX do mapa.
 */
export default function Map({ route }) {
  const [zoom, setZoom] = useState(18);
  const [center, setCenter] = useState(null);

  useEffect(() => {
    const getCenter = calculateCenterPoint(route);

    setCenter({
      lat: getCenter.latitude,
      lng: getCenter.longitude,
    });
  }, []);

  /**
   * Renderiza polilinhas no mapa.
   *
   * @param {Object} map - O objeto do mapa.
   * @param {Object} maps - O objeto do Google Maps.
   */
  const renderPolylines = (map, maps) => {
    const path = route.map((location) => {
      return new maps.LatLng(location["LATITUDE"], location["LONGITUDE"]);
    });

    const polyline = new maps.Polyline({
      path: path,
      geodesic: true,
      strokeColor: "#f44336",
      strokeOpacity: 1.0,
      strokeWeight: 2,
    });

    polyline.setMap(map);
  };

  if (!center) return <></>;

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: "" }}
        defaultCenter={center}
        defaultZoom={zoom}
        onChange={({ zoom }) => setZoom(zoom)}
        onGoogleApiLoaded={({ map, maps }) => renderPolylines(map, maps)}
        yesIWantToUseGoogleMapApiInternals
      >
        {route.map((location, index) => (
          <MapMarker
            key={`marker-${index}`}
            lat={location["LATITUDE"]}
            lng={location["LONGITUDE"]}
            label={location["SEQUENCIA"]}
            zoom={zoom}
          />
        ))}
      </GoogleMapReact>
    </div>
  );
}
