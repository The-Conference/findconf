import React from "react";
import "./main.scss";
import { Prev1, Prev2 } from "../Previews/Previews";
import Calendar from "../Calendar/Calendar";
import Greeting from "../Greeting/Greeting";
// import GreetingForAuth from "./Greeting/GreetingForAuth";
// import LoaderTemplate from "../../utils/Loader/LoaderTemplate";

const Main = ({ conferences }) => {
  return (
    <div className="main">
      <Greeting />
      {/* <GreetingForAuth /> */}
      <Calendar />
      <Prev1 />
      <Prev2 />
      {/* <LoaderTemplate /> */}
    </div>
  );
};

export default Main;
