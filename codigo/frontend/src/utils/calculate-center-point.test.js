/* eslint-disable no-undef */
import calculateCenterPoint from './calculate-center-point';

describe('calculateCenterPoint', () => {
  test('calcula o ponto central de um array de pontos', () => {
    const points = [
      { latitude: 10, longitude: 20 },
      { latitude: 20, longitude: 30 },
      { latitude: 30, longitude: 40 }
    ];
    const expected = { latitude: 20, longitude: 30 };
    const result = calculateCenterPoint(points);
    expect(result).toEqual(expected);
  });

  test('retorna zero quando o array está vazio', () => {
    const points = [];
    const expected = { latitude: 0, longitude: 0 };
    const result = calculateCenterPoint(points);
    expect(result).toEqual(expected);
  });

  test('calcula corretamente quando o array contém um único ponto', () => {
    const points = [{ latitude: 15, longitude: 25 }];
    const expected = { latitude: 15, longitude: 25 };
    const result = calculateCenterPoint(points);
    expect(result).toEqual(expected);
  });

  test('funciona com valores negativos e positivos de latitude e longitude', () => {
    const points = [
      { latitude: -10, longitude: 10 },
      { latitude: 10, longitude: -10 }
    ];
    const expected = { latitude: 0, longitude: 0 };
    const result = calculateCenterPoint(points);
    expect(result).toEqual(expected);
  });
});
