import React from "react";
import { Link } from "react-router-dom";
import "./registered.scss";
import welcome from "../../assets/welcome.svg";
const Registered = () => {
  return (
    <div className="registered">
      <div className="registered__container">
        <div className="registered__title">
          Ты часть <br /> <span>The Conference!</span>{" "}
        </div>

        <img className="registered__img" src={welcome} alt="welcome" />
        <Link className="registered__link" to="/login">
          <div className="registered__button"> Авторизоваться</div>
        </Link>
      </div>
    </div>
  );
};
export default Registered;
