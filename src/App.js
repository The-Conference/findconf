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

function App() {
  const [card, setCard] = useState(conferenceCard);
  const handleFollow = (id) => {
    setCard(
      card.map((el) => (el.id === id ? { ...el, follow: !el.follow } : el))
    );
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
                  card={card}
                  setCard={setCard}
                  handleFollow={handleFollow}
                />
              }
            />
            <Route
              path="/all"
              element={
                <All
                  card={card}
                  setCard={setCard}
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
