import React from "react";
import "./main.scss";
import { LoaderTemplateHeader } from "../../utils/Loader/LoaderTemplate";
import { Suspense } from "react";
// import GreetingForAuth from "./Greeting/GreetingForAuth";
// import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
const Calendar = React.lazy(() => import("../Calendar/Calendar"));
const Greeting = React.lazy(() => import("../Greeting/Greeting"));
const AllConferences = React.lazy(() => import("../Conference/AllConferences"));

const Main = () => {
  return (
    <div className="main">
      <Suspense fallback={<LoaderTemplateHeader />}>
        <Greeting />
        {/* <GreetingForAuth /> */}
        <Calendar />
        <AllConferences data={"prev1"} />
        <AllConferences data={"prev2"} />
        <AllConferences data={"prev3"} />
        {/* <LoaderTemplate /> */}
      </Suspense>
    </div>
  );
};

export default Main;
