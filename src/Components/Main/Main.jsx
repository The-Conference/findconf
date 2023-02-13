import React from "react";
import "./main.scss";
import UpPrev from "./Conference/UpPrev";
import PastPrev from "./Conference/PastPrev";
import AllPrev from "./Conference/AllPrev";
import Greeting from "./Greeting/Greeting";
import Calendar from "./Calendar/Calendar";

// import GreetingForAuth from "./Greeting/GreetingForAuth";
// import LoaderTemplate from "../../utils/Loader/LoaderTemplate";

const Main = () => {
  return (
    <div className="main">
      <Greeting />

      {/* <GreetingForAuth /> */}
      <Calendar />
      {/* <LoaderTemplate /> */}
      <UpPrev />
      <AllPrev />
      <PastPrev />
    </div>
  );
};

export default Main;
