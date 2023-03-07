import React from "react";
import "./footer.scss";
import logo from "../../assets/logo.svg";
const Footer = () => {
  return (
    <footer>
      <div className="footer">
        <img src={logo} alt="logo" />
        <p> &#169; The Conference 2023</p>
      </div>
    </footer>
  );
};
export default Footer;
