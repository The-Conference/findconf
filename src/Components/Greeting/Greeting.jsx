import React from "react";

import welcome from "../../assets/welcome2.svg";
import "./greeting.scss";
const Greeting = () => {
  return (
    <div className="greeting">
      <div className="greeting__text">
        <div className="greeting__text-first">Начни свой путь </div>
        <div className="greeting__text-second">с нашего сервиса</div>
        {/* <p>Мы помогаем студентам и профессионалам развиваться</p> */}
        <button className="greeting__button">
          <a href="/signup">Зарегистрироваться</a>
        </button>
      </div>
      <div className="greeting__pic">
        <img
          loading="lazy"
          src={welcome}
          alt="conference"
          width="372"
          height="265"
        />
        <button className="greeting__hidden">
          <a href="/signup">Зарегистрироваться</a>
        </button>
      </div>
    </div>
  );
};
export default Greeting;
