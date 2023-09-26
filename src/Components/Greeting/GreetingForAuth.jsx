import React from "react";
import greet from "../../assets/main.svg";
import "./greeting.scss";

const GreetingForAuth = () => {
  return (
    <div className="greeting">
      <div className="greeting__text" style={{ alignSelf: "center" }}>
        <h1 className="greeting__text-first" style={{ color: "#2C60E7" }}>
          С возвращением!{" "}
        </h1>

        <p>Мы подобрали для тебя несколько интересных конференций</p>
      </div>
      <div className="greeting__pic-a">
        <img
          className="greeting__pic-auth"
          loading="lazy"
          src={greet}
          alt="conference"
          width="372"
          height="265"
        />
      </div>
    </div>
  );
};
export default GreetingForAuth;
