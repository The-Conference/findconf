import React from "react";
import greet from "../../assets/main.svg";
import greet2 from "../../assets/main2.svg";
import "./greeting.scss";

const GreetingForAuth = () => {
  return (
    <div className="greeting">
      <div className="greeting__pic">
        <img src={greet} alt="conference" width="387" height="270" />
      </div>
      <div className="greeting__text" style={{ alignSelf: "center" }}>
        <h1 className="greeting__text-second">С возвращением! </h1>

        <p>Мы подобрали для тебя несколько интересных конференций</p>
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
export default GreetingForAuth;
