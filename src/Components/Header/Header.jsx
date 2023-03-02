import React from "react";
import logo from "../../assets/logo.svg";
import fave from "../../assets/favourite.svg";
import "./header.scss";
import SearchFilter from "../SearchFilter/SearchFilter";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header>
      <div className="header">
        <Link to="/">
          <div className="header__logo">
            <img src={logo} alt="logo" /> <span>THE CONF</span>
          </div>
        </Link>
        <SearchFilter />
        <nav className="header__nav">
          <ul>
            <Link to="/about">
              <li>О сервисе</li>
            </Link>
          </ul>
        </nav>
        <div>
          <div className="header__profile">
            <a href="/favourite">
              <div>
                <img src={fave} alt="favourite" />
              </div>
            </a>
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
