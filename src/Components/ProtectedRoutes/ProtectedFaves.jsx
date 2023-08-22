import React from "react";
import { useSelector } from "react-redux";
import AllConferences from "../Conference/AllConferences";
import Login from "../Login/Login";
import Header from "../Header/Header";
// import Footer from "../Footer/Footer";
const ProtectedFaves = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  return isAuthenticated ? (
    <>
      <Header />
      <AllConferences data={"favourites"} />
      {/* <Footer /> */}
    </>
  ) : (
    <Login />
  );
};

export default ProtectedFaves;
