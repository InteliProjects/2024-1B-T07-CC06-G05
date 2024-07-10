/* eslint-disable no-undef */
import { generateCsvContent } from './generate-csv-content';

describe('generateCsvContent', () => {
  test('gera o conteúdo CSV corretamente para dados complexos', () => {
    const data = {
      "2023-06-05": {
        "Rota A": {
          tempo: "2h",
          extensao: "5km",
          pontos: [
            { id: 1, endereco: "Rua A, 123", latitude: "-23.5505", longitude: "-46.6333", sequencia: 1 },
            { id: 2, endereco: "Rua B, 456", latitude: "-23.5515", longitude: "-46.6343", sequencia: 2 }
          ]
        }
      },
      "2023-06-06": {
        "Rota B": {
          tempo: "1h",
          extensao: "3km",
          pontos: [
            { id: 1, endereco: "Rua C, 789", latitude: "-23.5525", longitude: "-46.6353", sequencia: 1 }
          ]
        }
      }
    };

    const expectedCsvContent =
      "Dia,Rota,Tempo,Extensão,ID do Ponto,Endereço,Latitude,Longitude,Sequência\n" +
      "2023-06-05,Rota A,2h,5km,1,Rua A, 123,-23.5505,-46.6333,1\n" +
      "2023-06-05,Rota A,2h,5km,2,Rua B, 456,-23.5515,-46.6343,2\n" +
      "2023-06-06,Rota B,1h,3km,1,Rua C, 789,-23.5525,-46.6353,1";

    const result = generateCsvContent(data);
    expect(result).toBe(expectedCsvContent);
  });

  test('gera um CSV vazio quando não há dados', () => {
    const data = {};
    const expectedCsvContent = "Dia,Rota,Tempo,Extensão,ID do Ponto,Endereço,Latitude,Longitude,Sequência";
    const result = generateCsvContent(data);
    expect(result).toBe(expectedCsvContent);
  });
});
