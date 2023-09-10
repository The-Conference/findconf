import React, { Suspense } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { Provider } from "react-redux";
import store from "./store/store";
import ReactGA from "react-ga";
import { GAListener } from "./GAListener";
import SignUp from "./Components/SignUp/SignUp";
import Login from "./Components/Login/Login";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { LoaderTemplateHeader } from "./utils/Loader/LoaderTemplate";
import Registered from "./Components/SignUp/Registered";
import ProtectedFaves from "./Components/ProtectedRoutes/ProtectedFaves";
import Layout from "./Components/Layout/Layout";

const LazyHeader = React.lazy(() => import("./Components/Header/Header"));
// const LazyFooter = React.lazy(() => import("./Components/Footer/Footer"));
const LazyEmptyResult = React.lazy(() =>
  import("./Components/EmptyResult/EmptyResult")
);
const LazyNotFound = React.lazy(() => import("./Components/404/404"));
const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"main"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },
  {
    path: "/favourite",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <ProtectedFaves />
        </Suspense>
      </>
    ),
    redirectTo: "/login",
  },

  {
    path: "/conferences",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"conferences"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },
  {
    path: "/grants",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"grants"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },

  {
    path: "/conferences/:confId",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"full"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },
  {
    path: "/search/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"search"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },

  {
    path: "/search/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyEmptyResult />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },
  {
    path: "/about",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <Layout type={"about"} />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },

  {
    path: "/signup",
    element: (
      <>
        <SignUp />
      </>
    ),
  },
  {
    path: "/login",
    element: (
      <>
        <Login />
      </>
    ),
  },
  {
    path: "/users/activation/:uid/:token",
    element: (
      <>
        <Registered />
      </>
    ),
  },

  {
    path: "*",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyNotFound />
          {/* <LazyFooter /> */}
        </Suspense>
      </>
    ),
  },
]);
ReactGA.initialize("G-DQN3936RFH");

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Provider store={store}>
    <GAListener>
      <RouterProvider router={router} />
    </GAListener>
  </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
