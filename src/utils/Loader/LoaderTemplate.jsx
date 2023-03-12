import React from "react";
import Loader from "./Loader";
import LoaderHeader from "./LoaderHeader";

const LoaderTemplate = () => {
  return (
    <div>
      <Loader />
      <Loader />
    </div>
  );
};
export default LoaderTemplate;

export const LoaderTemplateTwo = () => {
  return (
    <div>
      <Loader />
    </div>
  );
};

export const LoaderTemplateHeader = () => {
  return (
    <div>
      <LoaderHeader />
      <Loader />
      <Loader />
    </div>
  );
};
