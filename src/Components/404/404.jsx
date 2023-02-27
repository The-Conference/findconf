import React from "react";
import notfound from "./404.svg";
const NotFound = () => {
  return (
    <div style={{ height: "100vh", maxWidth: "1220px", margin: "20px auto" }}>
      <img src={notfound} alt="не найдено" />
    </div>
  );
};

export default NotFound;
