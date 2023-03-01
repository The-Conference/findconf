import React from "react";
import "./main.scss";
import AllConferences from "../Conference/AllConferences";
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
      <AllConferences />
      {/* <LoaderTemplate /> */}
    </div>
  );
};

export default Main;
