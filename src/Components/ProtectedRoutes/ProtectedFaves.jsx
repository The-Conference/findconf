import React, { useState, useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import AllConferences from "../Conference/AllConferences";
import Login from "../Login/Login";
import Header from "../Header/Header";
// import Footer from "../Footer/Footer";
import FloatingMenu from "../FloatingMenu/FloatingMenu";
import SideBar from "../SideBar/SideBar";
import useOnClickOutside from "../Hooks/useOnClickOutside";
const ProtectedFaves = () => {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  const [menu, setMenu] = useState(false);
  const [focus, setFocus] = useState(false);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const ref = useRef();
  useOnClickOutside(ref, () => {
    setMenu(false);
    setFocus(false);
  });
  useEffect(() => {
    if (windowWidth > 861) {
      setFocus(false);
    }
    if (windowWidth <= 861 && menu) {
      setFocus(true);
    }
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [windowWidth, menu]);
  return isAuthenticated ? (
    <>
      {focus === true ? <div className="focus"></div> : null}
      <Header />
      <div className={menu ? "layout scroll-hidden" : "layout"} ref={ref}>
        <SideBar desktop={true} />
        <AllConferences data={"favourites"} />
        {menu ? <SideBar mobile={true} /> : null}
      </div>
      <FloatingMenu
        menu={menu}
        setMenu={setMenu}
        focus={focus}
        setFocus={setFocus}
      />
      {/* <Footer /> */}
    </>
  ) : (
    <Login />
  );
};

export default ProtectedFaves;
