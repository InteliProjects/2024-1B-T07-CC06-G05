/* eslint-disable no-undef */
import { sendData } from './sendData';

// Mock global do fetch
global.fetch = jest.fn();

describe('sendData', () => {
  // Configuração inicial antes de cada teste
  beforeEach(() => {
    fetch.mockClear();
  });

  // Teste para garantir que os dados sejam enviados com sucesso e a resposta JSON seja retornada
  test('envia dados com sucesso e retorna a resposta JSON', async () => {
    // Dados de exemplo a serem enviados
    const mockFormData = new FormData();
    mockFormData.append("key", "value");

    // Resposta simulada do servidor
    const mockJsonResponse = { message: 'Success' };
    fetch.mockResolvedValueOnce({
      ok: true,  // Indica que a requisição foi bem-sucedida
      json: () => Promise.resolve(mockJsonResponse),  // Simula a conversão da resposta para JSON
      text: () => Promise.resolve(JSON.stringify(mockJsonResponse))  // Simula a conversão da resposta para texto
    });

    // Chama a função sendData e verifica se a resposta é igual à resposta simulada
    const response = await sendData(mockFormData);
    expect(response).toEqual(mockJsonResponse);
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/sendData", {
      method: "POST",
      body: mockFormData,  // Dados enviados no corpo da requisição
    });
  });

  // Teste para garantir que a resposta seja tratada como texto se não for JSON
  test('trata a resposta como texto se a resposta não for JSON', async () => {
    const mockFormData = new FormData();
    const mockTextResponse = 'Server error';
    fetch.mockResolvedValueOnce({
      ok: false,  // Indica que a requisição não foi bem-sucedida
      json: () => Promise.reject(new Error('Not JSON')),  // Simula erro ao tentar converter a resposta para JSON
      text: () => Promise.resolve(mockTextResponse)  // Simula a conversão da resposta para texto
    });

    // Espera que a função sendData lance um erro com a mensagem especificada
    await expect(sendData(mockFormData)).rejects.toThrow("Failed to send data");
    expect(fetch).toHaveBeenCalled();  // Verifica se a função fetch foi chamada
  });

  // Teste para garantir que um erro seja lançado se a requisição falhar
  test('lança um erro se a requisição falhar', async () => {
    const mockFormData = new FormData();
    fetch.mockRejectedValueOnce(new Error('Network error'));  // Simula uma falha na requisição

    // Espera que a função sendData lance um erro com a mensagem especificada
    await expect(sendData(mockFormData)).rejects.toThrow("Failed to send data");
    expect(fetch).toHaveBeenCalled();  // Verifica se a função fetch foi chamada
  });
});
