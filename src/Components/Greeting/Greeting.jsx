import React from "react";
import greet from "../../assets/main.svg";
import greet2 from "../../assets/main2.svg";
import "./greeting.scss";
const Greeting = () => {
  return (
    <div className="greeting">
      <div className="greeting__pic">
        <img src={greet} alt="conference" width="387" height="270" />
      </div>
      <div className="greeting__text">
        <h1 className="greeting__text-first">Начни свой путь </h1>
        <h1 className="greeting__text-second">с нашего сервиса</h1>
        <p>Мы помогаем студентам и профессионалам развиваться</p>
        {/* <button>Зарегистрироваться</button> */}
      </div>
      <div className="greeting__pic">
        <img
          loading="lazy"
          src={greet2}
          alt="conference"
          width="372"
          height="265"
        />
      </div>
    </div>
  );
};
export default Greeting;
