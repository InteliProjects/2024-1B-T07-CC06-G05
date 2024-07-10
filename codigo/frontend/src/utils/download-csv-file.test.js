/**
 * @jest-environment jsdom
 */
/* eslint-disable no-undef */
import { downloadCsvFile } from './download-csv-file';

describe('downloadCsvFile', () => {
  test('cria e dispara o download de um arquivo CSV', () => {
    // Mock para document.createElement e URL.createObjectURL
    const createElementSpy = jest.spyOn(document, 'createElement');
    createElementSpy.mockImplementation(() => ({
      href: '',
      download: '',
      click: jest.fn(),
      setAttribute: jest.fn(),
    }));

    const createObjectURLSpy = jest.spyOn(URL, 'createObjectURL');
    createObjectURLSpy.mockReturnValue('blob:http://localhost/blobject');

    const revokeObjectURLSpy = jest.spyOn(URL, 'revokeObjectURL');
    revokeObjectURLSpy.mockImplementation(() => { });

    const appendChildSpy = jest.spyOn(document.body, 'appendChild').mockImplementation(() => { });
    const removeChildSpy = jest.spyOn(document.body, 'removeChild').mockImplementation(() => { });

    // Executar a função
    downloadCsvFile('nome,idade\nAlice,24', 'users.csv');

    // Verifica se um elemento 'a' foi criado corretamente
    expect(createElementSpy).toHaveBeenCalledWith('a');
    expect(createElementSpy.mock.results[0].value.download).toBe('users.csv');

    // Verifica se a URL do blob foi criada e atribuída corretamente
    expect(createObjectURLSpy).toHaveBeenCalled();
    expect(createElementSpy.mock.results[0].value.href).toBe('blob:http://localhost/blobject');

    // Verifica se o link foi clicado
    expect(createElementSpy.mock.results[0].value.click).toHaveBeenCalled();

    // Verifica se o link foi adicionado e removido do body
    expect(appendChildSpy).toHaveBeenCalledWith(createElementSpy.mock.results[0].value);
    expect(removeChildSpy).toHaveBeenCalledWith(createElementSpy.mock.results[0].value);

    // Verifica se a URL do blob foi revogada
    expect(revokeObjectURLSpy).toHaveBeenCalledWith('blob:http://localhost/blobject');

    // Limpeza dos mocks
    createElementSpy.mockRestore();
    createObjectURLSpy.mockRestore();
    revokeObjectURLSpy.mockRestore();
    appendChildSpy.mockRestore();
    removeChildSpy.mockRestore();
  });
});
