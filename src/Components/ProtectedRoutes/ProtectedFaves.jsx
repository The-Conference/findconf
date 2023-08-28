import React, { useState } from "react";
import { useSelector } from "react-redux";
import AllConferences from "../Conference/AllConferences";
import Login from "../Login/Login";
import Header from "../Header/Header";
// import Footer from "../Footer/Footer";
import FloatingMenu from "../FloatingMenu/FloatingMenu";
import SideBar from "../SideBar/SideBar";
const ProtectedFaves = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  const [menu, setMenu] = useState(false);
  return isAuthenticated ? (
    <>
      <Header />
      <div className="layout">
        <SideBar desktop={true} />
        <AllConferences data={"favourites"} />
        {menu ? <SideBar mobile={true} /> : null}
      </div>
      <FloatingMenu menu={menu} setMenu={setMenu} />
      {/* <Footer /> */}
    </>
  ) : (
    <Login />
  );
};

export default ProtectedFaves;
