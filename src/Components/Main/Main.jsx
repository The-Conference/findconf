import React from "react";
import "./main.scss";
import { Suspense } from "react";
import GreetingForAuth from "../Greeting/GreetingForAuth";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import { useSelector } from "react-redux";
import "../../Components/UI kit/Buttons.scss";
// const Calendar = React.lazy(() => import("../Calendar/Calendar"));
const Greeting = React.lazy(() => import("../Greeting/Greeting"));
const AllConferences = React.lazy(() => import("../Conference/AllConferences"));

const Main = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  return (
    <div className="main">
      <Suspense fallback={<LoaderTemplateTwo />}>
        {(isAuthenticated && <GreetingForAuth />) || <Greeting />}
        {/* <Calendar /> */}
        <AllConferences data={"prev1"} />
        <AllConferences data={"prev2"} />
        <AllConferences data={"prev3"} />
      </Suspense>
    </div>
  );
};

export default Main;
