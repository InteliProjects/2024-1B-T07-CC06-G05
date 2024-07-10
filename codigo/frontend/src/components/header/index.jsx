import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import styles from "./style.module.css";
import Menu from "../menu-but";

/**
 * Componente de cabeçalho.
 *
 * @returns {JSX.Element} O elemento JSX do cabeçalho.
 */
export default function Header() {
  const navigate = useNavigate();

  const [technicalColor, setTechnicalColor] = useState("#F0F0F0");
  const [comercialColor, setComercialColor] = useState("#0092B6");

  const handleTechnicalClick = () => {
    setTechnicalColor("#0092B6"); 
    setComercialColor("#F0F0F0");
    navigate('/technical');
  };

  const handleComercialClick = () => {
    setComercialColor("#0092B6");
    setTechnicalColor("#F0F0F0");
    navigate('');
  };

  return (
    <div className={styles.header}>
      <div className={styles.menu}>  
        <Menu 
          label={"Comercial"}
          onclick={handleComercialClick}
          style={{backgroundColor: comercialColor}}
        />
        <Menu 
          label = {"Técnico"}
          onclick={handleTechnicalClick}
          style={{backgroundColor: technicalColor}}
        />
      </div>
      <img
        src="aegea_logo.png"
        alt="Logo da Aegea Saneamento"
        className={styles.logo}
      />
    </div>
  );
}
