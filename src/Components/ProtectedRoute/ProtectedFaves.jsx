import React from "react";
import { useSelector } from "react-redux";
import AllConferences from "../Conference/AllConferences";
import Login from "../Login/Login";

const ProtectedFaves = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  return isAuthenticated ? (
    <>
      <AllConferences data={"favourites"} />
    </>
  ) : (
    <Login />
  );
};

export default ProtectedFaves;
