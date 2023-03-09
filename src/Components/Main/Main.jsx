import React from "react";
import "./main.scss";
import Calendar from "../Calendar/Calendar";
import Greeting from "../Greeting/Greeting";
import AllConferences from "../Conference/AllConferences";
// import GreetingForAuth from "./Greeting/GreetingForAuth";
// import LoaderTemplate from "../../utils/Loader/LoaderTemplate";

const Main = () => {
  return (
    <div className="main">
      <Greeting />
      {/* <GreetingForAuth /> */}
      <Calendar />
      <AllConferences data={"prev1"} />
      <AllConferences data={"prev2"} />
      <AllConferences data={"prev3"} />
      {/* <LoaderTemplate /> */}
    </div>
  );
};

export default Main;
