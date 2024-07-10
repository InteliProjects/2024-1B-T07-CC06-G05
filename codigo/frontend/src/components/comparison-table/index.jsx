import styles from "./style.module.css";
import WhiteBackground from "../white-background";
import React, { useState, useEffect } from "react";

function toCSV(data) {
  const csvRows = [];
  const headers = Object.keys(data[0]);
  csvRows.push(headers.join(','));

  for (const row of data) {
      const values = headers.map(header => {
          const escaped = ('' + row[header]).replace(/"/g, '\\"');
          return `"${escaped}"`;
      });
      csvRows.push(values.join(','));
  }

  return csvRows.join('\n');
}

/**
 * Renderiza um componente de tabela de comparação.
 * @param {Object} props - As propriedades do componente.
 * @param {Array} props.data - Os dados a serem exibidos na tabela de comparação.
 * @param {Object} props.filteringSettings - As configurações de filtro para a tabela.
 * @returns {JSX.Element} O componente de tabela de comparação.
 */
export default function Comparisons({ data, filteringSettings }) {
  const [sortedData, setSortedData] = useState(data);

  const noFiltering = filteringSettings.orderBy === "";

  useEffect(() => {
    if (!noFiltering) {
      let sorted = [...data];
      sorted.sort((a, b) => {
        if (filteringSettings.order === "asc") {
          return a[filteringSettings.orderBy] > b[filteringSettings.orderBy] ? 1 : -1;
        } else {
          return a[filteringSettings.orderBy] < b[filteringSettings.orderBy] ? 1 : -1;
        }
      });
      setSortedData(sorted);
    } else {
      setSortedData(data);
    }
  }, [data, filteringSettings, noFiltering]);

  /**
   * Lida com o download dos resultados em um arquivo CSV.
   * @param {Object} data - Os dados para download.
   */
  const handleDownloadResults = (data) => {
    const flatData = [];
    data.pontos.forEach((ponto) => {
      flatData.push({
        Logradouro: ponto.LOGRADOURO,
        Numero: ponto.NUMERO,
        Sequencia: ponto.SEQUENCIA,
        Latitude: ponto.LATITUDE,
        Longitude: ponto.LONGITUDE,
      });
    });

    const csvData = toCSV(flatData);

    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'resultados.csv');
    document.body.appendChild(a);
    a.click();
  };

  return (
    <div className={styles.comparisonGrid}>
      {sortedData.map((data) => (
        <WhiteBackground id="routes-background" width="20vw" height="40vh">
          <div className={styles.container}>
            <div className={styles.content_container}>
              <p className={styles.title}>{data.rota}</p>
              <p className={styles.content}>Distância total: <br/>{data.tamanho}</p>
              <p className={styles.content}>Tempo de execução:  <br/>{parseFloat(data.tempo) > 11 ? <span style={{color: 'red'}}>Acima de 6 horas</span> : <span style={{color: 'green'}}>Dentro do limite</span>}</p>
            </div>
            <button className={styles.submit} onClick={() => handleDownloadResults(data)}>
              Baixar CSV
            </button>
          </div>
        </WhiteBackground>
      ))}
    </div>
  );
}
