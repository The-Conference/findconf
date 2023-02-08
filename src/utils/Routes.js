import React from "react";
import Login from "../Components/Login/Login";
import SignUp from "../Components/SignUp/SignUp";

const ROUTES = [
  { path: "/login", component: <Login /> },
  { path: "/signup", component: <SignUp /> },
];

export default ROUTES;
