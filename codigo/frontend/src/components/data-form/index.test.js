/* eslint-disable no-undef */
import { render, fireEvent, waitFor } from '@testing-library/react';
import DataForm from './index';
import { sendData } from '../../services/send-data.service';

// Mock do serviço sendData
jest.mock('../../services/send-data.service');

describe('DataForm', () => {
  const mockSetData = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza o formulário corretamente', () => {
    const { getByLabelText } = render(<DataForm setData={mockSetData} />);
    const inputFile = getByLabelText("Insira os dados (CSV):");
    expect(inputFile).toBeInTheDocument();
  });

  test('atualiza o estado ao inserir um arquivo', () => {
    const { getByLabelText } = render(<DataForm setData={mockSetData} />);
    const inputFile = getByLabelText("Insira os dados (CSV):");
    const file = new File(['content'], 'example.csv', { type: 'text/csv' });

    fireEvent.change(inputFile, { target: { files: [file] } });

    // Verificar se o input de arquivo tem um arquivo após a mudança
    expect(inputFile.files[0]).toBe(file);
    expect(inputFile.files.item(0)).toBe(file);
  });

  test('exibe um alerta se tentar enviar sem arquivo', () => {
    window.alert = jest.fn();
    const { getByText } = render(<DataForm setData={mockSetData} />);
    fireEvent.click(getByText('Enviar'));
    expect(window.alert).toHaveBeenCalledWith("Por favor, insira um arquivo CSV antes de enviar.");
  });

  test('envia dados quando o formulário é submetido com um arquivo', async () => {
    sendData.mockResolvedValue('Dados enviados com sucesso');
    const { getByLabelText, getByText } = render(<DataForm setData={mockSetData} />);
    const inputFile = getByLabelText("Insira os dados (CSV):");
    const file = new File(['content'], 'example.csv', { type: 'text/csv' });

    fireEvent.change(inputFile, { target: { files: [file] } });
    fireEvent.click(getByText('Enviar'));

    await waitFor(() => {
      expect(sendData).toHaveBeenCalledWith(file);
      expect(mockSetData).toHaveBeenCalledWith('Dados enviados com sucesso');
    });
  });
});
