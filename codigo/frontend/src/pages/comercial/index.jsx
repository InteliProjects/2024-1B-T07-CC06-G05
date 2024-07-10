import { useEffect, useState } from "react";
import styles from "./style.module.css";
import Routes from "../../components/routes";
import Table from "../../components/table";
import { getResults } from "../../services/get-results.service";

/**
 * Componente de painel de controle.
 *
 * @returns {JSX.Element} O componente de painel de controle.
 */
export default function Comercial() {
  const [routesData, setRoutesData] = useState(null);
    useEffect(() => {
      let ignore = false;
      getResults().then(result => {
        if (!ignore) { 
          setRoutesData(result);
        }
      })
    return () => { ignore = true; }
    }, [])

  const [currentRoute, setCurrentRoute] = useState(1);

  return (
    <div className={styles.dashboard}>
      <div className={styles.data_and_results}>
        <Routes data={routesData} route={currentRoute} setRoute={setCurrentRoute} />
      </div>
      <Table data={routesData} route={currentRoute} />
    </div>
  );
}
