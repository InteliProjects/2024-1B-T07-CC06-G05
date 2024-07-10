import WhiteBackground from "../../components/white-background";
import ExportButton from "../export-routes";
import Map from "../map";
import styles from "./style.module.css";

/**
 * Componente de rotas.
 *
 * @component
 * @param {Object} props - As propriedades do componente.
 * @param {Object} props.data - Os dados recebidos para exibição.
 * @param {int} props.route - Rota atual para exibição.
 * @param {Function} props.setRoute - Função para alterar a rota atual em exibição.
 * @param {Function} props.retryGetResults - Função para tentar obter os resultados do backend.
 * @returns {JSX.Element} O elemento JSX que representa o componente de rotas.
 */
export default function Routes({ data, route, setRoute, retryGetResults }) {
  const receivedError = typeof data === "string";
  const waitingResponse = data === "Executing algorithm.";
  const emptyData = !data;

  const handleChangePage = (next) => {
    const nextPage = next > 0 && route < Object.keys(data).length;
    const previousPage = next < 0 && route > 1;
    if (nextPage || previousPage) {
      setRoute(route + next)
    }
  }

  if (waitingResponse) { setTimeout(retryGetResults, 60000 * 60); }
  return (
    <WhiteBackground
      id="routes-background"
      width="95%"
      height="75vh"
      padding="3vh"
    >
      <div className={styles.container}>
        {waitingResponse ? (
          <img src="loading.gif" alt="Gif de carregamento" className={styles.loading} />
        ) : receivedError ? (
          <p className={styles.no_data}>{data}</p>
        ) : emptyData ? (
          <p className={styles.no_data}>Sem dados para mostrar</p>
        ) : (
          // Se não está carregando, nem recebeu um erro e os dados não estão vazios (requisição foi um sucesso)
          <>
            <Map route={data["Rota " + route]["Pontos"]} />
            <div className={styles.change_page_container}>
              <button className={styles.change_page_button} onClick={() => handleChangePage(-1)}>
                <img src="left_arrow.svg" alt="Seta para esquerda" className={styles.change_page_arrow} />
              </button>
              <button className={styles.change_page_button} onClick={() => handleChangePage(1)}>
                <img src="right_arrow.svg" alt="Seta para direita" className={styles.change_page_arrow} />
              </button>
            </div>
            <ExportButton data={data} />
          </>
        )}
      </div>
    </WhiteBackground>
  );
}
