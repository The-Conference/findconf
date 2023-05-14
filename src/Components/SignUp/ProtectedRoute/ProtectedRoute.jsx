import React from "react";
import { useSelector } from "react-redux";
import Profile from "../../Profile/Profile";
import Login from "../../Login/Login";
import Header from "../../Header/Header";
import Footer from "../../Footer/Footer";
const ProtectedRoute = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  return (
    <>
      {(isAuthenticated && (
        <>
          <Header />
          <Profile />
          <Footer />
        </>
      )) || <Login />}
    </>
  );
};

export default ProtectedRoute;
