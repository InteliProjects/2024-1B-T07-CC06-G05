const API_URL = "http://127.0.0.1:8000/sendData";

/**
 * Envia dados para o servidor usando uma requisição POST.
 * 
 * @param {FormData} formData - Os dados a serem enviados.
 * @returns {Promise} A promessa que resolve para os dados da resposta, que pode ser um JSON ou um texto simples.
 * @throws {Error} Se tiver falhado ao enviar os dados.
 */
export async function sendData(formData) {
  try {
    // Executa uma requisição POST com os dados fornecidos no corpo da requisição
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    // Recupera o tipo de conteúdo da resposta para determinar como processá-la
    const contentType = response.headers.get("content-type");

    // Decide se a resposta deve ser tratada como JSON ou como texto simples
    // A resposta é tratada como JSON apenas se a requisição foi bem-sucedida e o tipo de conteúdo é JSON
    const data = await (response.ok && contentType && contentType.indexOf("application/json") !== -1 ? response.json() : response.text());

    // Retorna os dados da resposta, que podem ser um objeto JSON ou uma string de texto
    return data;
  } catch (error) {
    // Registra o erro no console para fins de depuração
    console.error("Error sending data: ", error);

    // Lança um novo erro indicando falha ao enviar os dados
    throw new Error("Failed to send data.");
  }
}
