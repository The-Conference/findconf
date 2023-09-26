import React from "react";
import "./main.scss";
import { Suspense } from "react";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import "../../Components/UI kit/Buttons.scss";
// const Calendar = React.lazy(() => import("../Calendar/Calendar"));
const AllConferences = React.lazy(() => import("../Conference/AllConferences"));
const Main = () => {
  return (
    <div className="main">
      <Suspense fallback={<LoaderTemplateTwo />}>
        {/* <Calendar /> */}
        <AllConferences data={"prev"} />
      </Suspense>
    </div>
  );
};

export default Main;
