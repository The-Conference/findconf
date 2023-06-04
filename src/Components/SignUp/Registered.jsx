import React from "react";
import { Link } from "react-router-dom";
const Registered = () => {
  return (
    <>
      <div>Ты часть The Conference!</div>
      <Link to="/login">Авторизоваться</Link>
    </>
  );
};
export default Registered;
