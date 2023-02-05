import React from "react";
import logo from "./logo.png";
import "./header.scss";
import search from "./searchgrey.svg";

const Header = () => {
  return (
    <header>
      <div className="header">
        <div className="header__logo">
          <img src={logo} alt="logo" />
        </div>
        <div className="header__search">
          <img src={search} alt="search" role="button" />
          <input type="text" placeholder="Тема конференции, организатор" />
        </div>

        <nav className="header__nav">
          <ul>
            <li>План конференции</li>
            <li>О нас</li>
          </ul>
        </nav>
        <button className="header__signin">Войти</button>
      </div>
    </header>
  );
};
export default Header;
