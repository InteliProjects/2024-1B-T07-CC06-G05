import React from 'react';
import "./style.module.css";

/**
 * Componente de tabela.
 *
 * @component
 * @param {Object} props - As propriedades do componente.
 * @param {Object} props.data - Os dados da tabela.
 * @param {int} props.route - Os dados da tabela.
 * @returns {JSX.Element} O elemento da tabela.
 */
export default function Table({ data, route }) {
  if (data === null || typeof data === "string")  { return null; }
  const headers = ["Rota", "Tempo", "Extensão", "#"];
  const fields  = ["Índice", "Logradouro", "Número", "Sequência"]

  return (
    <table>
      <thead>
        <tr>
          {headers.map((header) => (
            <th key={header}>{header}</th>
          ))}
        </tr>
        <tr>
          <td key={"Rota " + route}>{"Rota " + route}</td>
          <td key={"Tempo" + route}>{parseFloat(data["Rota " + route]["Tempo"].substring(0, data["Rota " + route]["Tempo"].length - 1)).toFixed(2) + "h"}</td>
          <td key={"Tamanho" + route}>{parseFloat(data["Rota " + route]["Tamanho"].substring(0, data["Rota " + route]["Tamanho"].length - 2)).toFixed(2) + "km"}</td>
          <td key="#">#</td>
        </tr>
        <tr>
          {fields.map((field) => (
            <th key={field}>{field}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data["Rota " + route]["Pontos"].map((ponto, index) => (
          <tr key={index}>
            <td>{ponto["INDICE"]}</td>
            <td>{ponto["LOGRADOURO"]}</td>
            <td>{ponto["NUMERO"]}</td>
            <td>{ponto["SEQUENCIA"]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
