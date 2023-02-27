import "./App.css";
import React from "react";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import Main from "./Components/Main/Main";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchFilteredConferences } from "./store/postData";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchFilteredConferences());
  }, []);

  return (
    <div className="App">
      <Header />
      <Main />
      <Footer />
    </div>
  );
}

export default App;
