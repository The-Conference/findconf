import React from "react";
import Loader from "./Loader";
import LoaderHeader from "./LoaderHeader";

const LoaderTemplate = () => {
  return (
    <div>
      <LoaderHeader />
      <Loader />
      <Loader />
      <Loader />
      <Loader />
    </div>
  );
};
export default LoaderTemplate;
