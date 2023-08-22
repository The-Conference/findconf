import React from "react";
import logo from "../../assets/logo.svg";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import "./header.scss";
import { fetchOnce, reset } from "../../store/postData";
import SearchFilter from "../SearchFilter/SearchFilter";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../../store/authSlice";
import { Star, Bell, Search } from "iconoir-react";
const Header = () => {
  const dispatch = useDispatch();
  const nav = useNavigate();
  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  const handleLogOut = () => {
    dispatch(logout());
    dispatch(reset());

    nav("/");

    dispatch(fetchOnce());
  };
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
            {/* <li>
              <Link to="/about">О сервисе </Link>
            </li> */}
            <li>
              <div className="header__profile">
                <div>
                  <Bell
                    style={{ cursor: "pointer" }}
                    title="Уведомления"
                    height={24}
                    width={24}
                  />
                </div>
              </div>
            </li>

            <li>
              {(isAuthenticated && (
                <a href="/favourite">
                  <div className="header__profile">
                    <div>
                      <Star
                        style={{ cursor: "pointer" }}
                        title="Избранное"
                        height={24}
                        width={24}
                      />
                    </div>
                  </div>
                </a>
              )) ||
                null}
            </li>
            <li className="header__signin">
              {(!isAuthenticated && <Link to="/login">Войти </Link>) || (
                <button onClick={handleLogOut}>Выйти</button>
              )}
            </li>
            <li className="header__search">
              <div className="header__profile">
                <div>
                  <Search
                    style={{ cursor: "pointer" }}
                    title="Найти"
                    height={24}
                    width={24}
                  />
                </div>
              </div>
            </li>
          </ul>
        </nav>

        {/* <a href="/login">
          <button className="header__signin">Войти</button>
        </a> */}
      </div>
    </header>
  );
};
export default Header;
