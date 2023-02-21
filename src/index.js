import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { Provider } from "react-redux";
import store from "./store/store";
import { Suspense } from "react";
import LoaderTemplate from "./utils/Loader/LoaderTemplate";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import FullConference from "./Components/FullConference/FullConference";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SearchResult from "./Components/SearchResult/SearchResult";

const Login = React.lazy(() => import("./Components/Login/Login"));
const SignUp = React.lazy(() => import("./Components/SignUp/SignUp"));
const All = React.lazy(() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(import("./Components/Main/Conference/AllConferences"));
    }, 1000);
  });
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/all",
    element: (
      <>
        <Header />
        <All />
        <Footer />
      </>
    ),
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
  {
    path: "/conferences/:itemId",
    element: (
      <>
        <Header />
        <FullConference />
        <Footer />
      </>
    ),
  },
  {
    path: "/search/:value",
    element: (
      <>
        <Header />
        <SearchResult />
        <Footer />
      </>
    ),
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Suspense fallback={<LoaderTemplate />}>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </Suspense>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
