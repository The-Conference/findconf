import React from "react";
import logo from "./logo.png";
import search from "./search.svg";
import "./header.scss";
import fave from "./favourite.svg";

const HeaderForAuth = () => {
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
        <div className="header__profile">
          <div>
            <img src={fave} alt="favourite" />
          </div>
          <button>Профиль</button>{" "}
        </div>
      </div>
    </header>
  );
};

export default HeaderForAuth;
