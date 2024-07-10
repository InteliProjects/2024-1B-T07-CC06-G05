const API_URL = "http://127.0.0.1:8000/getResults";

/**
 * Consulta os resultados no servidor a partir de uma requisição GET.
 * 
 * A função faz uma chamada HTTP GET para o servidor usando a URL definida.
 * A resposta pode ser JSON ou texto, dependendo do tipo de conteúdo recebido.
 * 
 * @returns {Promise} A promessa que resolve para os dados da resposta, podendo ser um objeto JSON ou texto.
 * @throws {Error} Se tiver falhado ao enviar os dados ou processar a resposta.
 */
export async function getResults() {
    try {
      // Realiza a requisição GET ao servidor
      const response = await fetch(API_URL, {
        method: "GET"
      });

      const data = await tryParseJson(response);

      // Retorna os dados processados
      return data;
    } catch (error) {
      // Registra o erro no console para fins de depuração
      console.error("Error getting results: ", error);

      // Lança um erro indicando que houve falha ao obter os resultados
      throw new Error("Failed to get results.");
  }
}

async function tryParseJson(response) {
  try {
    const objString = await response.clone().json(); 
    return JSON.parse(objString);
  }
  catch {
    response
    return await response.text();
  }
}