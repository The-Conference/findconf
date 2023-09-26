import React from "react";
import logo from "../../assets/logo.svg";
import "./header.scss";
const Logo = () => {
  return (
    <a href="/">
      <div className="header__logo">
        <img loading="lazy" src={logo} alt="logo" width="57" height="44" />
        <span>THE CONF</span>
      </div>
    </a>
  );
};
export default Logo;
