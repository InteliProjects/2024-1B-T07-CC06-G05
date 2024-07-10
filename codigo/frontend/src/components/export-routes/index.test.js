/* eslint-disable no-undef */
import { render, fireEvent } from '@testing-library/react';
import ExportButton from './index';
import { generateCsvContent } from '../../utils/generate-csv-content';
import { downloadCsvFile } from '../../utils/download-csv-file';

// Mock das funções de utilitários
jest.mock('../../utils/generate-csv-content');
jest.mock('../../utils/download-csv-file');

describe('ExportButton', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('clica no botão de exportar e dispara a geração e download do CSV', () => {
    // Preparar dados e mocks
    generateCsvContent.mockReturnValue('conteúdo,csv');
    const { getByText } = render(<ExportButton />);

    // Simular o clique
    fireEvent.click(getByText('Exportar Dados'));

    // Verifica se as funções foram chamadas corretamente
    expect(generateCsvContent).toHaveBeenCalled();
    expect(downloadCsvFile).toHaveBeenCalledWith('conteúdo,csv', 'dados_exportados.csv');
  });

  test('exibe um alerta se não houver dados para exportar', () => {
    // Redefinindo o mock para retornar undefined
    generateCsvContent.mockReturnValue(undefined);
    window.alert = jest.fn();

    const { getByText } = render(<ExportButton />);

    // Simular o clique
    fireEvent.click(getByText('Exportar Dados'));

    // Verifica se o alerta foi chamado
    expect(window.alert).toHaveBeenCalledWith("Nenhum dado disponível para exportar");
    expect(downloadCsvFile).not.toHaveBeenCalled();  // Verifica se o download não foi iniciado
  });
});
