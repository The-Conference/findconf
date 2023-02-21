import React from "react";
import logo from "./logo.png";
import "./header.scss";
import fave from "./favourite.svg";
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
        <div>
          <div className="header__profile">
            <div>
              <img src={fave} alt="favourite" />
            </div>
          </div>
        </div>
        {/* <a href="/login">
          <button className="header__signin">Войти</button>
        </a> */}
      </div>
    </header>
  );
};
export default Header;
