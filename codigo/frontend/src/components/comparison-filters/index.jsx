import React from "react"; // Importa React
import { useState } from "react"; // Importa o hook useState do React
import WhiteBackground from "../white-background"; // Importa o componente WhiteBackground
import styles from "./style.module.css"; // Importa os estilos do CSS

/**
 * Componente de formulário de dados.
 *
 * @param {Object} props - As propriedades do componente.
 * @param {Function} props.setfilterData - Função para definir os dados filtrados.
 * @returns {JSX.Element} O elemento do formulário de dados.
 */
export default function ComparisonFilters({ setfilterData }) {

  // Declara um estado chamado OrderState e uma função setOrderState para atualizá-lo
  const [OrderState, setOrderState] = useState({
    orderBy: "", // Campo de ordenação
    order: "",   // Direção da ordenação
  });

  // Função para atualizar um campo específico no estado OrderState
  const updateField = (field, value) => {
    setOrderState((prev) => ({ ...prev, [field]: value }));
  };

  // Função chamada ao aplicar a ordenação
  const handleOrderChange = () => {
    setfilterData(OrderState); // Chama a função passada via props para definir os dados filtrados
  };

  return (
    <WhiteBackground
      id="data-form-background" // ID do componente
      width="25vw"              // Largura do componente
      height="35vh"             // Altura do componente
      padding="3vh"             // Padding do componente
    >
      <form id="data-form" className={styles.data_form}>
        <label htmlFor="orderBy" className={styles.label}>
          Ordenar por: {/* Rótulo para o campo de ordenação */}
        </label>
        <select
          name="orderBy"
          id="orderBy"
          value={OrderState.orderBy} // Valor atual do campo de ordenação
          onChange={(e) => updateField("orderBy", e.target.value)} // Atualiza o estado ao mudar o valor
          className={styles.select}
        >
          <option value="">Selecione</option>
          <option value="D_total">Distancia total</option>
          <option value="tempo_exec">Tempo de execução</option>
        </select>

        <label htmlFor="order" className={styles.label}>
          Direção da ordenação: {/* Rótulo para o campo de direção da ordenação */}
        </label>
        <select
          name="order"
          id="order"
          value={OrderState.order} // Valor atual do campo de direção da ordenação
          onChange={(e) => updateField("order", e.target.value)} // Atualiza o estado ao mudar o valor
          className={styles.select}
        >
          <option value="">Selecione</option>
          <option value="asc">Crescente</option>
          <option value="desc">Decrescente</option>
        </select>
      </form>
      <button onClick={handleOrderChange} className={styles.submit}>
        Filtrar {/* Botão para aplicar o filtro */}
      </button>
    </WhiteBackground>
  );
}
