import "./App.css";
import React, { useEffect } from "react";
import Main from "./Components/Main/Main";
import { useDispatch } from "react-redux";
import { fetchFilteredConferences } from "./store/postData";
import ReactGA from "react-ga";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchFilteredConferences());
  }, [dispatch]);
  useEffect(() => {
    ReactGA.pageview(window.location.pathname + window.location.search);
  }, []);

  return (
    <div className="App">
      <Main />
    </div>
  );
}

export default App;
