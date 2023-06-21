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
import AboutService from "./Components/AboutService/AboutService";
import ProtectedRoute from "./Components/ProtectedRoute/ProtectedRoute";

const LazyHeader = React.lazy(() => import("./Components/Header/Header"));
const LazyApp = React.lazy(() => import("./App"));
const LazyAllConferences = React.lazy(() =>
  import("./Components/Conference/AllConferences")
);
const LazyFullConference = React.lazy(() =>
  import("./Components/FullConference/FullConference")
);
const LazyFooter = React.lazy(() => import("./Components/Footer/Footer"));
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
          <LazyApp />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },
  {
    path: "/favourite/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"favourites"} />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },
  {
    path: "/all",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"all"} />
          <LazyFooter />
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
          <LazyFullConference />
          <LazyFooter />
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
          <LazyAllConferences data={"search-results"} />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },
  {
    path: "/collection2/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"collection2"} />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },
  {
    path: "/collection1/",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"collection1"} />
          <LazyFooter />
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
          <LazyFooter />
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
          <AboutService />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },

  {
    path: "/date/:date",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"date"} />
          <LazyFooter />
        </Suspense>
      </>
    ),
  },
  {
    path: "/dates/:periods",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"periods"} />
          <LazyFooter />
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
    path: "/profile",
    element: (
      <>
        <ProtectedRoute />
      </>
    ),
    redirectTo: "/login",
  },

  {
    path: "*",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyNotFound />
          <LazyFooter />
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
