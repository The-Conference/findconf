import React from "react";
import "./footer.scss";
import logo from "../../assets/logo.svg";
const Footer = () => {
  return (
    <footer>
      <div className="footer">
        <a href="/">
          <img src={logo} alt="logo" />
        </a>
        <a href="/about">О сервисе</a>
        <p> &#169;2023 сервис The Conference </p>
      </div>
    </footer>
  );
};
export default Footer;
