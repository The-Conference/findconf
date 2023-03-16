import React from "react";
import "./main.scss";
import { Suspense } from "react";
// import GreetingForAuth from "./Greeting/GreetingForAuth";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
const Calendar = React.lazy(() => import("../Calendar/Calendar"));
const Greeting = React.lazy(() => import("../Greeting/Greeting"));
const AllConferences = React.lazy(() => import("../Conference/AllConferences"));

const Main = () => {
  return (
    <div className="main">
      <Suspense fallback={<LoaderTemplateTwo />}>
        {/* <LoaderTemplateHeader /> */}
        <Greeting />
        {/* <GreetingForAuth /> */}
        <Calendar />
        <AllConferences data={"prev1"} />
        <AllConferences data={"prev2"} />
        <AllConferences data={"prev3"} />
      </Suspense>
    </div>
  );
};

export default Main;
