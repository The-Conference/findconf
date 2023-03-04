import React from "react";
import greet from "../../assets/main.svg";
import "./greeting.scss";

const Greeting = () => {
  return (
    <div className="greeting">
      <div className="greeting__pic">
        <img src={greet} alt="man with laptop" />
      </div>
      <div className="greeting__text">
        <h1 className="greeting__text-first">Начни свой путь </h1>
        <h1 className="greeting__text-second">с нашего сервиса</h1>
        <p>Мы помогаем студентам и профессионалам развиваться</p>
        {/* <button>Зарегистрироваться</button> */}
      </div>
      <div className="greeting__pic">
        <img src={greet} alt="man with laptop" />
      </div>
    </div>
  );
};
export default Greeting;
