import React from "react";
import logo from "../../assets/logo.svg";
import fave from "../../assets/favourite.svg";
import "./header.scss";
import SearchFilter from "../SearchFilter/SearchFilter";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header style={{ padding: "0 20px" }}>
      <div className="header">
        <a href="/">
          <div className="header__logo">
            <img loading="lazy" src={logo} alt="logo" width="57" height="44" />
            <span>THE CONF</span>
          </div>
        </a>
        <SearchFilter />
        <nav className="header__nav">
          <ul>
            <li>
              <Link to="/about">О сервисе </Link>
            </li>
          </ul>
        </nav>
        <div>
          <div className="header__profile">
            <a href="/favourite">
              <div>
                <img
                  loading="lazy"
                  src={fave}
                  alt="favourite"
                  width="20"
                  height="19"
                />
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
