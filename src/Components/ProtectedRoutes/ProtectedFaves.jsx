import React from "react";
import { useSelector } from "react-redux";
import AllConferences from "../Conference/AllConferences";
import Login from "../Login/Login";
import Header from "../Header/Header";
// import Footer from "../Footer/Footer";
import FloatingMenu from "../FloatingMenu/FloatingMenu";
import SideBar from "../SideBar/SideBar";
const ProtectedFaves = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  return isAuthenticated ? (
    <>
      <Header />
      <div className="layout">
        <SideBar />
        <AllConferences data={"favourites"} />
      </div>
      <FloatingMenu />
      {/* <Footer /> */}
    </>
  ) : (
    <Login />
  );
};

export default ProtectedFaves;
