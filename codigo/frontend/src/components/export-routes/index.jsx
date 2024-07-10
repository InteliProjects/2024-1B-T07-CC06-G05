import styles from "./style.module.css";
import { generateCsvContent } from "../../utils/generate-csv-content";
import { downloadCsvFile } from "../../utils/download-csv-file";

/**
 * Componente de botão de exportação.
 *
 * @returns {JSX.Element} O elemento JSX do botão de exportação.
 */
export default function ExportButton({ data }) {
  const handleExport = () => {
    if (!data) {
      alert("Nenhum dado disponível para exportar");
      return;
    }
    
    const csvContent = generateCsvContent(data);
    downloadCsvFile(csvContent, "dados_exportados.csv");
  };

  return (
    <button onClick={handleExport} className={styles.submit}>
      Exportar Dados
    </button>
  );
}
