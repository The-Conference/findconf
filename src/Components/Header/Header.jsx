import React from "react";
import logo from "./logo.png";
import "./header.scss";
import SearchFilter from "../SearchFilter/SearchFilter";

const Header = () => {
  return (
    <header>
      <div className="header">
        <a href="/">
          <div className="header__logo">
            <img src={logo} alt="logo" />
          </div>
        </a>
        <SearchFilter />
        <nav className="header__nav">
          <ul>
            <li>О сервисе</li>
          </ul>
        </nav>
        <a href="/login">
          <button className="header__signin">Войти</button>
        </a>
      </div>
    </header>
  );
};
export default Header;
