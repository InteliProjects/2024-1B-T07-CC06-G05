/**
 * Baixa um arquivo CSV com o conteúdo e o nome fornecidos.
 *
 * @param {string} content - O conteúdo do arquivo CSV.
 * @param {string} filename - O nome do arquivo a ser baixado.
 */
export function downloadCsvFile(content, filename) {
  const blob = new Blob([content], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
