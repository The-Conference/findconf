import React from "react";
import greet from "./greeting.svg";
import "./greeting.scss";

const GreetingForAuth = () => {
  return (
    <div className="greeting">
      <img src={greet} alt="man with laptop" />
      <div className="greeting__text-auth">
        <h1>С возвращением!</h1>
        <p>
          Мы нашли несколько новых конференций для тебя! Они уже ждут твоего
          участия
        </p>
        {/* <button>Зарегистрироваться</button> */}
      </div>
      <img src={greet} alt="man with laptop" />
    </div>
  );
};
export default GreetingForAuth;
