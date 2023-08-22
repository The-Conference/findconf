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
import Registered from "./Components/SignUp/Registered";
import ProtectedFaves from "./Components/ProtectedRoutes/ProtectedFaves";
import FloatingMenu from "./Components/FloatingMenu/FloatingMenu";
const LazyHeader = React.lazy(() => import("./Components/Header/Header"));
const LazyApp = React.lazy(() => import("./App"));
const LazyAllConferences = React.lazy(() =>
  import("./Components/Conference/AllConferences")
);
const LazyFullConference = React.lazy(() =>
  import("./Components/FullConference/FullConference")
);
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
          <LazyApp />
          {/* <LazyFooter /> */}
          <FloatingMenu />
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
          <FloatingMenu />
        </Suspense>
      </>
    ),
    redirectTo: "/login",
  },

  {
    path: "/all",
    element: (
      <>
        <Suspense fallback={<LoaderTemplateHeader />}>
          <LazyHeader />
          <LazyAllConferences data={"all"} />
          <FloatingMenu />
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
          <LazyFullConference />
          <FloatingMenu />
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
          <LazyAllConferences data={"search-results"} />
          <FloatingMenu />
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
          <FloatingMenu />
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
          <AboutService />
          <FloatingMenu />
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
