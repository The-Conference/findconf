import React from "react";
import styles from "./footer.module.scss";
import logo from "../../assets/logo.svg";
const Footer = () => {
  return (
    <footer>
      <div className={styles.footer}>
        <a href="/">
          <img src={logo} alt="logo" width="20" height="19" />
        </a>
        <a href="/about">О сервисе</a>
        <p> &#169;2023 сервис The Conference </p>
      </div>
    </footer>
  );
};
export default Footer;
