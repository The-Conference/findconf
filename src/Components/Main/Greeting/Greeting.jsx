import React from "react";
import greet from "./greeting.svg";
import "./greeting.scss";

const Greeting = () => {
  return (
    <div className="greeting">
      <img src={greet} alt="man with laptop" />
      <div className="greeting__text">
        <p>Мы помогаем студентам и профессионалам развиваться</p>
        <h1 className="greeting__text-first">Начни свой путь </h1>
        <h1 className="greeting__text-second">с нашего сервиса</h1>
        <button>Зарегистрироваться</button>
      </div>
      <img src={greet} alt="man with laptop" />
    </div>
  );
};
export default Greeting;
