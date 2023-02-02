import React from "react";
import "./main.scss";

import Calendar from "./Calendar/Calendar.tsx";
import UpPrev from "./Conference/UpPrev";
import PastPrev from "./Conference/PastPrev";
import AllPrev from "./Conference/AllPrev";
import Greeting from "./Greeting/Greeting";

const Main = ({ card, setCard, handleFollow }) => {
  return (
    <div className="main">
      <Greeting />
      <Calendar />
      <UpPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <AllPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <PastPrev card={card} setCard={setCard} handleFollow={handleFollow} />
    </div>
  );
};

export default Main;
