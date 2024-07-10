import styles from "./style.module.css";

/**
 * Componente de fundo branco.
 *
 * @component
 * @param {string} id - O id do elemento div.
 * @param {string} width - A largura do elemento div.
 * @param {string} height - A altura do elemento div.
 * @param {string} padding - O espaçamento interno do elemento div.
 * @param {string} minHeight - A altura mínima do elemento div.
 * @param {number} zIndex - O índice de empilhamento do elemento div.
 * @param {ReactNode} children - Os elementos filhos do componente.
 * @returns {JSX.Element} O componente de fundo branco.
 */
export default function WhiteBackground({
  id,
  width,
  height,
  padding,
  minHeight,
  zIndex,
  children,
}) {
  return (
    <div
      id={id}
      className={styles.white_bg}
      style={{
        width: width,
        height: height,
        padding: padding,
        minHeight: minHeight,
        zIndex: zIndex,
      }}
    >
      {children}
    </div>
  );
}
