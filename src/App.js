import "./App.css";
import Main from "./Components/Main/Main";
import Footer from "./Components/Footer/Footer";
import Header from "./Components/Header/Header";
// import HeaderForAuth from "./Components/Header/HeaderForAuth";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Suspense } from "react";
import React from "react";
import LoaderTemplate from "./utils/Loader/LoaderTemplate";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const Up = React.lazy(() =>
  import("./Components/Main/Conference/UpcomingConference")
);
const Past = React.lazy(() =>
  import("./Components/Main/Conference/PastConference")
);
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
    element: <Main />,
  },
  {
    path: "/all",
    element: <All />,
  },
  {
    path: "/finished",
    element: <Past />,
  },
  {
    path: "/upcoming",
    element: <Up />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
]);

function App() {
  return (
    <div className="App">
      {/* <HeaderForAuth /> */}
      <Suspense fallback={<LoaderTemplate />}>
        <Header />
        <RouterProvider router={router} />
        <Footer />
      </Suspense>
    </div>
  );
}

export default App;

// const LIMIT = 8;
//.slice(0, LIMIT)
// const [visible, setVisible] = useState(LIMIT);
// const [hasMore, setHasMore] = useState(true);
// const fetchData = () => {
//   const newLimit = visible + LIMIT;
//   const dataToAdd = conferenceCard.slice(visible, newLimit);

//   if (conferenceCard.length > postData.length) {
//     setTimeout(() => {
//       setPostData([...postData].concat(dataToAdd));
//     }, 1000);
//     setVisible(newLimit);
//   } else {
//     setHasMore(false);
//   }
// };
