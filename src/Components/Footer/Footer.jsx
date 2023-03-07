import React from "react";
import "./footer.scss";
import logo from "../../assets/logo.svg";
const Footer = () => {
  return (
    <footer className="footer">
      <img src={logo} alt="logo" />
      <p> &#169; Copyright 2023</p>
    </footer>
  );
};
export default Footer;
