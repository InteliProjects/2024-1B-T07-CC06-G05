import React, { useState } from 'react';
import styles from "./style.module.css";

/**
 * Componente do botão de menu
 *
 * @returns {JSX.Element} O elemento JSX do menu.
 */

export default function Menu({label, onclick, style}) {

    return (
        <button className={styles.button} onClick={onclick} style={style}>
            Menu {label}
        </button>
    );
}