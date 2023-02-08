import React from "react";
import "./main.scss";
import UpPrev from "./Conference/UpPrev";
import PastPrev from "./Conference/PastPrev";
import AllPrev from "./Conference/AllPrev";
// import Greeting from "./Greeting/Greeting";
import Calendar from "./Calendar/Calendar";
import GreetingForAuth from "./Greeting/GreetingForAuth";
// import LoaderTemplate from "../../utils/Loader/LoaderTemplate";

const Main = ({ handleFollow, postData }) => {
  return (
    <div className="main">
      {/* <Greeting /> */}

      <GreetingForAuth />
      <Calendar />
      {/* <LoaderTemplate /> */}
      <UpPrev handleFollow={handleFollow} postData={postData} />
      <AllPrev handleFollow={handleFollow} postData={postData} />
      <PastPrev handleFollow={handleFollow} postData={postData} />
    </div>
  );
};

export default Main;
