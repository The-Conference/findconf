import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import "./header.scss";
import { fetchOnce, reset } from "../../store/postData";
import SearchFilter from "../SearchFilter/SearchFilter";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../../store/authSlice";
import { Star, Bell, Search } from "iconoir-react";
import Logo from "./Logo";
const Header = () => {
  const dispatch = useDispatch();
  const nav = useNavigate();
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  const handleLogOut = () => {
    dispatch(logout());
    dispatch(reset());

    nav("/");

    dispatch(fetchOnce());
  };
  const [focused, setFocused] = useState(false);
  useEffect(() => {
    if (windowWidth > 861) {
      setFocused(false);
    }
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [windowWidth]);
  return (
    <>
      {(focused && (
        <SearchFilter mobile={true} focused={focused} setFocused={setFocused} />
      )) || (
        <header style={{ padding: "0 20px" }}>
          <div className="header">
            <Logo />
            <SearchFilter
              desktop={true}
              focused={focused}
              setFocused={setFocused}
            />

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
                        onClick={() => setFocused(true)}
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
      )}
    </>
  );
};
export default Header;
