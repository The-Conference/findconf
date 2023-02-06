import "./App.css";
import Main from "./Components/Main/Main";
import { useState } from "react";
import conferenceCard from "./utils/mock";
import Footer from "./Components/Footer/Footer";
// import Header from "./Components/Header/Header";
import HeaderForAuth from "./Components/Header/HeaderForAuth";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Suspense } from "react";
import React from "react";
import LoaderTemplate from "./utils/Loader/LoaderTemplate";

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
        <HeaderForAuth />
        <Suspense fallback={<LoaderTemplate />}>
          <Routes>
            <Route
              path="/"
              element={
                <Main
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
          </Routes>
        </Suspense>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
