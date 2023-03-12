import React from "react";
import "./main.scss";
import { LoaderTemplateHeader } from "../../utils/Loader/LoaderTemplate";
import { Suspense } from "react";
// import GreetingForAuth from "./Greeting/GreetingForAuth";

const Calendar = React.lazy(() => import("../Calendar/Calendar"));
const Greeting = React.lazy(() => import("../Greeting/Greeting"));
const AllConferences = React.lazy(() => import("../Conference/AllConferences"));

const Main = () => {
  return (
    <div className="main">
      <Suspense fallback={<LoaderTemplateHeader />}>
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
