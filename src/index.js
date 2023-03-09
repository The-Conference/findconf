import React, { Suspense } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { Provider } from "react-redux";
import store from "./store/store";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoaderTemplate from "./utils/Loader/LoaderTemplate";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import AboutService from "./Components/AboutService/AboutService";
import AllConferences from "./Components/Conference/AllConferences";
import NotFound from "./Components/404/404";
import EmptyResult from "./Components/EmptyResult/EmptyResult";
import FullConference from "./Components/FullConference/FullConference";
const Login = React.lazy(() => import("./Components/Login/Login"));
const SignUp = React.lazy(() => import("./Components/SignUp/SignUp"));

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/favourite",
    element: (
      <>
        <Header />
        <AllConferences data={"favourites"} />
        <Footer />
      </>
    ),
  },
  {
    path: "/all",
    element: (
      <>
        <Header />
        <AllConferences data={"all"} />
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
    path: "/conferences/:confId",
    element: (
      <>
        <Header />
        <FullConference />
        <Footer />
      </>
    ),
  },
  {
    path: "/search/",
    element: (
      <>
        <Header />
        <AllConferences data={"search-results"} />
        <Footer />
      </>
    ),
  },
  {
    path: "/collection2/",
    element: (
      <>
        <Header />
        <AllConferences data={"collection2"} />
        <Footer />
      </>
    ),
  },
  {
    path: "/collection1/",
    element: (
      <>
        <Header />
        <AllConferences data={"collection1"} />
        <Footer />
      </>
    ),
  },

  // {
  //   path: "/search/:value",
  //   element: (
  //     <>
  //       <Header />
  //       <SearchResult />
  //       <Footer />
  //     </>
  //   ),
  // },
  {
    path: "/search/",
    element: (
      <>
        <Header />
        <EmptyResult />
        <Footer />
      </>
    ),
  },
  {
    path: "/about",
    element: (
      <>
        <Header />
        <AboutService />
        <Footer />
      </>
    ),
  },
  {
    path: "/date/:date",
    element: (
      <>
        <Header />
        <AllConferences data={"date"} />
        <Footer />
      </>
    ),
  },
  {
    path: "/dates/:periods",
    element: (
      <>
        <Header />
        <AllConferences data={"periods"} />
        <Footer />
      </>
    ),
  },
  {
    path: "*",
    element: (
      <>
        <Header />
        <NotFound />
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
