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
import AboutService from "./Components/AboutService/AboutService";
import AllConferences from "./Components/Main/Conference/AllConferences";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SearchResult from "./Components/SearchResult/SearchResult";
import Favourites from "./Components/Favourite/Favourite";
import NotFound from "./Components/404/404";
import SearchDate from "./SearchDate/SearchDate";
const Login = React.lazy(() => import("./Components/Login/Login"));
const SignUp = React.lazy(() => import("./Components/SignUp/SignUp"));
const Full = React.lazy(() =>
  import("./Components/FullConference/FullConference")
);

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
        <Favourites />
        <Footer />
      </>
    ),
  },
  {
    path: "/all",
    element: (
      <>
        <Header />
        <AllConferences />
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
        <Full />
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
    path: "/conferences/dates/:date",
    element: (
      <>
        <Header />
        <SearchDate />
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