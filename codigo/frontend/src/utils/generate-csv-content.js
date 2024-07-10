/**
 * Gera o conteúdo de um arquivo CSV com base nos dados fornecidos.
 *
 * @param {Object} data - Os dados a serem convertidos em CSV.
 * @returns {string} O conteúdo do arquivo CSV gerado.
 */
export function generateCsvContent(data) {
  const headers = ["ROTA", "TEMPO", "EXTENSAO", "INDICE", "LOGRADOURO", "NUMERO", "LATITUDE", "LONGITUDE", "SEQUENCIA"];
  const csvRows = [headers];

  Object.entries(data).forEach(([routeName, routeDetails]) => {
    const entries = Object.entries(routeDetails)
    entries[2][1].forEach((point) => {
      csvRows.push([routeName, entries[0][1], entries[1][1],
        point["INDICE"], point["LOGRADOURO"], point["NUMERO"], point["LATITUDE"], point["LONGITUDE"], point["SEQUENCIA"]]);
    })
  });

  return csvRows.map(row => row.join(",")).join("\n");
}
