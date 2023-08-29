import React from "react";
import { sidebar_menu } from "../../utils/sidebar_menu";
import "./sidebar.scss";
import "./sidebar-mobile.scss";
import { Wallet } from "iconoir-react";
import Logo from "../Header/Logo";
const SideBar = ({ desktop, mobile }) => {
  const activePage = window.location.pathname;

  return (
    <>
      <div className={desktop ? "sidebar" : "sidebar-mobile visible fadeIn"}>
        <ul className="sidebar-menu">
          {mobile ? <Logo /> : null}
          {sidebar_menu.map((item, index) => (
            <li
              className={
                activePage === item.link
                  ? "sidebar-menu-item active"
                  : "sidebar-menu-item"
              }
              key={index}
            >
              <span className="sidebar-menu-icon">{item.icon}</span>
              <a className="sidebar-menu-link" href={item.link}>
                {item.text}
              </a>
            </li>
          ))}
        </ul>
        <div className="sidebar-footer">
          <button className="sidebar-footer-button">
            <Wallet />
            <span className="sidebar-footer-text">Поддержи нас :)</span>
          </button>
          <hr className="sidebar-footer-hr" />
          <ul className="sidebar-footer-list">
            <li className="sidebar-footer-item">
              <a href="/about" className="sidebar-footer-link">
                О сервисе
              </a>
            </li>
            <li className="sidebar-footer-item">
              <a href="/support" className="sidebar-footer-link">
                Поддержка
              </a>
            </li>
            <li className="sidebar-footer-item">
              <a href="/rules" className="sidebar-footer-link">
                Правила
              </a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};
export default SideBar;
