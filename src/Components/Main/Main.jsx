import React from "react";
import { Header } from "./Header/Header";
import Calendar from "./Calendar/Calendar.tsx";
import UpPrev from "./Conference/UpPrev";
import PastPrev from "./Conference/PastPrev";
import AllPrev from "./Conference/AllPrev";

const Main = ({ card, setCard, handleFollow }) => {
  return (
    <div>
      <Header />
      <Calendar />
      <UpPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <PastPrev card={card} setCard={setCard} handleFollow={handleFollow} />
      <AllPrev card={card} setCard={setCard} handleFollow={handleFollow} />
    </div>
  );
};

export default Main;
