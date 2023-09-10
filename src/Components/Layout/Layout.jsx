import React, { useState, useRef, useEffect } from "react";
import SideBar from "../SideBar/SideBar";
import App from "../../App";
import AllConferences from "../Conference/AllConferences";
import FloatingMenu from "../FloatingMenu/FloatingMenu";
import AboutService from "../AboutService/AboutService";
import FullConference from "../FullConference/FullConference";
import useOnClickOutside from "../Hooks/useOnClickOutside";
const Layout = ({ type }) => {
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
      setMenu(false);
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
  return (
    <>
      {focus === true ? <div className="focus"></div> : null}
      <div className={menu ? "layout scroll-hidden" : "layout"} ref={ref}>
        <SideBar desktop={true} />
        {type === "main" && <App />}
        {type === "conferences" && <AllConferences data={"all"} />}
        {type === "grants" && <AllConferences data={"grants"} />}
        {type === "about" && <AboutService />}
        {type === "full" && <FullConference />}
        {type === "search" && <AllConferences data={"search-results"} />}
        {menu ? <SideBar mobile={true} /> : null}
      </div>

      <FloatingMenu
        menu={menu}
        setMenu={setMenu}
        focus={focus}
        setFocus={setFocus}
      />
    </>
  );
};
export default Layout;
// export const LayoutConferences = (data) => {
//   return (
//     <div className="layout">
//       <SideBar desktop={true} />
//       <SideBar mobile={true} />
//       <AllConferences data={data} />
//     </div>
//   );
// };
