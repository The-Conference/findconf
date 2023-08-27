import React from "react";
import Greeting from "../Greeting/Greeting";
import GreetingForAuth from "../Greeting/GreetingForAuth";
import { useSelector } from "react-redux";
const Title = ({ data }) => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  return (
    <>
      {data !== "prev4" &&
        (<>{(isAuthenticated && <GreetingForAuth />) || <Greeting />}</> ||
          null)}
    </>
  );
};
export default Title;
