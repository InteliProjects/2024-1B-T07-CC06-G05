import React from "react";
import { useEffect, useState } from "react";
import WhiteBackground from "../../components/white-background";
import styles from "./style.module.css";
import { sendData } from "../../services/send-data.service";
import { getAlgorithms } from "../../services/get-algorithms.service";

/**
 * Componente de formulário de dados.
 *
 * @param {Object} props - As propriedades do componente.
 * @param {Function} props.setData - Função para definir os dados.
 * @returns {JSX.Element} O elemento do formulário de dados.
 */
export default function DataForm({ setData }) {
  const [formData, setFormData] = useState({
    filePresent: false,
    data: null,
    days: 22,
    leituras: 200,
    algorithm: 1,
    antIterations: 1000,
    alpha: 1,
    beta: 2,
    iterations: 500,
    pollinationIterations: 30,
    probability: 0.05,
    radius: 0.07
  });

  const algorithmsParams = [
    // Ant Colony Parameters
    { antIterations: "Iterações do Ant Colony",
      alpha: "Alfa (fator de priorização dos caminhos mais escolhidos)",
      beta: "Beta (fator de priorização de menores distâncias)"
    },
    
    // Pollination Parameters
    {
      pollinationIterations: "Iterações do Pollination",
      probability: "Probabilidade de troca",
      radius: "Raio de busca local"
    },

    // Ant Colony + 2-Opt Parameters
    { antIterations: "Iterações do Ant Colony",
      alpha: "Alfa (fator de priorização dos caminhos mais escolhidos)",
      beta: "Beta (fator de priorização de menores distâncias)",
      iterations: "Iterações do 2-Opt"
    },

    // Pollination + 2-Opt Parameters
    {
      pollinationIterations: "Iterações do Pollination",
      probability: "Probabilidade de troca",
      radius: "Raio de busca local",
      iterations: "Iterações do 2-Opt"
    },
  ]



  const [algorithms, setAlgorithms] = useState([])

  useEffect(() => {
    let ignore = false;
    getAlgorithms().then(result => {
      if (!ignore) { 
        setAlgorithms(result["algorithms"]);
      }
      })
    return () => {ignore = true};
  }, [])


  const updateField = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const checkInsertedFile = (event) => {
    updateField("filePresent", event.target.value !== "");
    updateField("data", event.target.files[0]);
  };

  const handleSendData = async () => {
    if (!formData.data) {
      alert("Por favor, insira um arquivo CSV antes de enviar.");
      return;
    }

    try {
      const responseData = await sendData(new FormData(document.getElementById("data-form")));
      setData(responseData);
    } catch (error) {
      console.log(error)
      alert("Erro ao enviar os dados.");
    }
  };

  return (
    <WhiteBackground
      id="data-form-background"
      width="25vw"
      minHeight="75vh"
      height="fit-content"
      padding="3vh"
    >
      <form id="data-form" className={styles.data_form}>
        <label htmlFor="data" className={styles.label}>
          Insira os dados (CSV):
        </label>
        <input
          name="data"
          id="data"
          type="file"
          accept=".csv"
          className={styles.input_file}
          style={
            formData.filePresent
              ? { color: "#192135", backgroundColor: "#ddd" }
              : {}
          }
          onChange={checkInsertedFile}
        />
        {/* Adiciona inputs para os outros campos usando o estado do formulário */}
        {Object.entries({
          days: "Máximo de dias de leitura",
          leituras: "Pontos a serem lidos por dia",
        }).map(([key, label]) => (
          <React.Fragment key={key}>
            <label htmlFor={key} className={styles.label}>
              {label}:
            </label>
            <input
              name={key}
              id={key}
              type="number"
              value={formData[key]}
              onChange={(e) => updateField(key, e.target.value)}
            />
          </React.Fragment>
        ))}
        {/* Adiciona inputs para parâmetros do algoritmo selecionado */}
        {Object.entries(algorithmsParams[formData.algorithm-1]).map(([key, value]) => (
          <React.Fragment key={key}>
            <label htmlFor={key} className={styles.label}>
              {value}:
            </label>
            <input
              name={key}
              id={key}
              type="number"
              value={formData[key]}
              onChange={(e) => updateField(key, e.target.value)}
            />
          </React.Fragment>
        ))}
        {/* Adiciona um dropdown para os algoritmos */}
        <label htmlFor={"algorithm"} className={styles.label}>
              Algoritmo utilizado:
        </label>
        <select
        name={"algorithm"}
        id={"algorithm"}
        value={formData["algorithm"]}
        onChange={(e) => updateField("algorithm", e.target.value)}
        >
          {algorithms.map((obj) => (
            <React.Fragment key={Object.keys(obj)[0]}>
            <option value={Object.values(obj)[0]}>{Object.keys(obj)[0]}</option>
          </React.Fragment>
          ))}
        </select>
        
      </form>
      <button type="submit" onClick={handleSendData} className={styles.submit}>
        Enviar
      </button>
    </WhiteBackground>
  );
}
