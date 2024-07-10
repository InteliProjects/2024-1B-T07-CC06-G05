/**
 * Calcula o ponto central de um conjunto de pontos.
 *
 * @param {Array} points - Um array contendo os pontos a serem calculados.
 * @returns {Object} - Um objeto contendo as coordenadas do ponto central.
 */
function calculateCenterPoint(points) {
  let totalLat = 0;
  let totalLng = 0;
  const numPoints = points.length;

  points.forEach(point => {
    totalLat += point['LATITUDE'];
    totalLng += point['LONGITUDE'];
  });

  const centerLat = totalLat / numPoints;
  const centerLng = totalLng / numPoints;

  return { latitude: centerLat, longitude: centerLng };
}

export default calculateCenterPoint;