import { useState, useEffect } from "react";
import styles from "./style.module.css";
import ComparisonFilters from "../../components/comparison-filters";
import ComparisonGrid from "../../components/comparison-table";
import { getResults } from "../../services/get-results.service";

/**
 * Componente de painel de controle.
 *
 * @returns {JSX.Element} O componente de painel de controle.
 */
export default function Comparison() {
  const [filterData, setfilterData] = useState({
    "orderBy": "",
    "order": ""
  });
  const [data, setData] = useState([]); 
  useEffect(() => {
    let ignore = false;
    getResults().then(result => {
      if (!ignore) {
        const formattedData = Object.keys(result).map(key => ({
          rota: key,
          tempo: result[key].Tempo,
          tamanho: result[key].Tamanho,
          pontos: result[key].Pontos
        }));
        setData(formattedData);
      }
    })
  return () => { ignore = true; }
  }, [])

  return (
    <div className={styles.dashboard}>
      <div className={styles.data_and_results}>
        <ComparisonFilters className={styles.filter} setfilterData={setfilterData} />
        {data.length > 0 ? (
          <ComparisonGrid data={data} filteringSettings={filterData} />
        ) : (
          <p>Carregando dados...</p>
        )}
      </div>
    </div>
  );
}