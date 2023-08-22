import React, { useState, useEffect } from "react";
import "./FloatingMenu.scss";
import { HomeAlt, User, Bell, Star } from "iconoir-react";

const FloatingMenu = () => {
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
          <a href="/">
            <Bell width={24} height={24} />
          </a>
        </li>
        <li>
          <a href="/favourite">
            <Star width={24} height={24} />
          </a>
        </li>
        <li>
          <a href="/">
            <User width={24} height={24} />
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default FloatingMenu;
