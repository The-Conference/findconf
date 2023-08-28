import React, { useState, useEffect } from "react";
import "./FloatingMenu.scss";
import { HomeAlt, User, Bell, Star } from "iconoir-react";

const FloatingMenu = ({ menu, setMenu, focus, setFocus }) => {
  const [isMenuFixed, setIsMenuFixed] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsMenuFixed(window.pageYOffset > 0);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <nav className={`floating-menu ${isMenuFixed ? "fixed" : ""}`}>
      <ul>
        <li>
          <a href="/">
            <HomeAlt width={24} height={24} />
          </a>
        </li>
        <li>
          <Bell width={24} height={24} />
        </li>
        <li>
          <a href="/favourite">
            <Star width={24} height={24} />
          </a>
        </li>
        <li
          onClick={() => {
            setMenu(!menu);
            setFocus(!focus);
          }}
        >
          <User width={24} height={24} />
        </li>
      </ul>
    </nav>
  );
};

export default FloatingMenu;
