import React from "react";
import "./main.scss";
import Greeting from "./Greeting/Greeting";
import Calendar from "./Calendar/Calendar";
import AllConferences from "./Conference/AllConferences";

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
