/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
import React from 'react';  // Importação necessária para usar JSX
import { render } from '@testing-library/react';
import Map from './Map';
import calculateCenterPoint from '../../utils/calculate-center-point';
import GoogleMapReact from 'google-map-react';

// Mock das funções e componentes externos
jest.mock('../../utils/calculate-center-point');
jest.mock('google-map-react', () => ({
  __esModule: true,
  default: ({ children, onGoogleApiLoaded }) => {
    // Simular a carga da API do Google Maps
    const map = {}; // Objeto mock do mapa
    const maps = {
      LatLng: jest.fn((lat, lng) => ({ lat, lng })),
      Polyline: jest.fn(() => ({
        setMap: jest.fn(),
      })),
    };
    onGoogleApiLoaded({ map, maps });

    return <div>{children}</div>;
  },
}));

describe('Map', () => {
  beforeEach(() => {
    // Resetar os mocks antes de cada teste
    jest.clearAllMocks();
    calculateCenterPoint.mockReturnValue({ latitude: 10, longitude: 20 });
  });

  test('renderiza o mapa com o centro e polilinhas corretamente', () => {
    const route = [
      { latitude: 10, longitude: 20, sequencia: 'A' },
      { latitude: 15, longitude: 25, sequencia: 'B' },
    ];

    const { getByText } = render(<Map route={route} />);

    // Verifica se as crianças (marcadores) são renderizadas
    expect(getByText('A')).toBeInTheDocument();
    expect(getByText('B')).toBeInTheDocument();

    // Verifica se a função de cálculo do centro foi chamada corretamente
    expect(calculateCenterPoint).toHaveBeenCalledWith(route);

    // Verifica se as funções do Google Maps foram chamadas
    expect(GoogleMapReact.mock.calls[0][0].onGoogleApiLoaded).toBeDefined();
  });
});
