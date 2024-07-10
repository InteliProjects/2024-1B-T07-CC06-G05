const API_URL = "http://127.0.0.1:8000/getAlgorithms";

/**
 * Consulta os algoritmos no servidor a partir de uma requisição GET.
 * 
 * Realiza uma chamada HTTP GET para o servidor usando a URL definida acima.
 * Processa a resposta dependendo do tipo de conteúdo: como JSON se for 'application/json'
 * e como texto plano se for qualquer outro tipo.
 * 
 * @returns {Promise} A promessa que resolve para os dados da resposta, que podem ser JSON ou texto.
 * @throws {Error} Se ocorrer falha na requisição ou no processamento da resposta.
 */
export async function getAlgorithms() {
    try {
      // Envio da requisição GET para o servidor para obter informações sobre os algoritmos
      const response = await fetch(API_URL, {
        method: "GET"
      });

      // Extração do tipo de conteúdo da resposta para determinar como ela deve ser processada
      const contentType = response.headers.get("content-type");

      // Processamento da resposta:
      // Se a resposta for bem-sucedida e o conteúdo for tipo JSON
      // caso contrário, retorna como texto.
      const data = await (response.ok && contentType && contentType.indexOf("application/json") !== -1 ? 
                          response.json() : 
                          response.text());

      // Retorno dos dados processados como JSON ou texto
      return data;
    } catch (error) {
      // Registro do erro no console para fins de depuração
      console.error("Error getting algorithms: ", error);

      // Lançamento de um erro para indicar falha na obtenção dos dados
      throw new Error("Failed to get algorithms.");
    }
  }
