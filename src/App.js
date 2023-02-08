import "./App.css";
import Main from "./Components/Main/Main";
import { useState } from "react";
import conferenceCard from "./utils/mock";
import Footer from "./Components/Footer/Footer";
import Header from "./Components/Header/Header";
// import HeaderForAuth from "./Components/Header/HeaderForAuth";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Suspense } from "react";
import React from "react";
import LoaderTemplate from "./utils/Loader/LoaderTemplate";
import Login from "./Components/Login/Login";
import SignUp from "./Components/SignUp/SignUp";

const Conf = React.lazy(() => import("./Components/Main/Main"));
const All = React.lazy(() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(import("./Components/Main/Conference/AllConferences"));
    }, 1000);
  });
});
const LIMIT = 8;
function App() {
  const [postData, setPostData] = useState(conferenceCard.slice(0, LIMIT));
  const [visible, setVisible] = useState(LIMIT);
  const [hasMore, setHasMore] = useState(true);

  const handleFollow = (id) => {
    setPostData(
      postData.map((el) => (el.id === id ? { ...el, follow: !el.follow } : el))
    );
  };
  const fetchData = () => {
    const newLimit = visible + LIMIT;
    const dataToAdd = conferenceCard.slice(visible, newLimit);

    if (conferenceCard.length > postData.length) {
      setTimeout(() => {
        setPostData([...postData].concat(dataToAdd));
      }, 1000);
      setVisible(newLimit);
    } else {
      setHasMore(false);
    }
  };

  return (
    <div className="App">
      <Router>
        {/* <HeaderForAuth /> */}
        <Header />
        <Suspense fallback={<LoaderTemplate />}>
          <Routes>
            <Route
              path="/"
              element={
                <Conf
                  postData={postData}
                  fetchData={fetchData}
                  handleFollow={handleFollow}
                />
              }
            />
            <Route
              path="/all"
              element={
                <All
                  postData={postData}
                  hasMore={hasMore}
                  fetchData={fetchData}
                  handleFollow={handleFollow}
                />
              }
            />

            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
          </Routes>
        </Suspense>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
