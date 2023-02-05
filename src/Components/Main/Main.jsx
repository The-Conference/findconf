import React from "react";
import "./main.scss";
import UpPrev from "./Conference/UpPrev";
import PastPrev from "./Conference/PastPrev";
import AllPrev from "./Conference/AllPrev";
// import Greeting from "./Greeting/Greeting";
import Calendar from "./Calendar/Calendar";
import GreetingForAuth from "./Greeting/GreetingForAuth";

const Main = ({ card, setCard, handleFollow }) => {
  return (
    <div className="main">
      {/* <Greeting /> */}
      <GreetingForAuth />
      <Calendar card={card} />
      <UpPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <AllPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <PastPrev card={card} setCard={setCard} handleFollow={handleFollow} />
    </div>
  );
};

export default Main;
