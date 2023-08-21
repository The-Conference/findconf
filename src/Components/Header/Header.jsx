import React from "react";
import logo from "../../assets/logo.svg";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import "./header.scss";
import { fetchOnce, reset } from "../../store/postData";
import SearchFilter from "../SearchFilter/SearchFilter";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../../store/authSlice";

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
            <li>
              <Link to="/about">О сервисе </Link>
            </li>

            <li>
              {(!isAuthenticated && <Link to="/login">Войти </Link>) || (
                <button onClick={handleLogOut}>Выйти</button>
              )}
            </li>
            <li>
              {(isAuthenticated && (
                <a href="/favourite">
                  <div className="header__profile">
                    <div>
                      <svg
                        width="20"
                        height="20"
                        viewBox="-1 0 22 18"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M9.99997 18.7501C9.89397 18.7501 9.78793 18.728 9.68893 18.683C9.36193 18.534 1.66598 14.9651 0.431976 8.60906C-0.0450242 6.15006 0.433982 3.75105 1.71298 2.19305C2.74798 0.931045 4.23594 0.260029 6.01694 0.251029C6.02594 0.251029 6.03494 0.251029 6.04294 0.251029C8.07494 0.251029 9.31399 1.40806 9.99899 2.39306C10.687 1.40406 11.9359 0.242029 13.9809 0.251029C15.7629 0.260029 17.2519 0.931045 18.2879 2.19305C19.5649 3.75005 20.0429 6.14904 19.5649 8.61004C18.3329 14.966 10.6359 18.5361 10.3089 18.6841C10.2119 18.7281 10.106 18.7501 9.99997 18.7501ZM6.04196 1.75005C6.03596 1.75005 6.03099 1.75005 6.02499 1.75005C4.68699 1.75605 3.62702 2.22503 2.87302 3.14403C1.87402 4.36103 1.513 6.29705 1.905 8.32305C2.86 13.247 8.59297 16.447 9.99997 17.165C11.407 16.447 17.14 13.247 18.094 8.32305C18.488 6.29605 18.127 4.36003 17.13 3.14403C16.376 2.22603 15.3159 1.75803 13.9749 1.75103C13.9689 1.75103 13.963 1.75103 13.958 1.75103C11.586 1.75103 10.745 4.12806 10.711 4.22906C10.607 4.53206 10.3209 4.73803 10.0009 4.73803C9.99895 4.73803 9.99792 4.73803 9.99692 4.73803C9.67592 4.73703 9.38993 4.53204 9.28793 4.22704C9.25493 4.12704 8.41296 1.75005 6.04196 1.75005Z"
                          fill="#2C60E7"
                        />
                      </svg>
                    </div>
                  </div>
                </a>
              )) ||
                null}
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
