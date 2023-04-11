import "./App.css";
import React, { useEffect } from "react";
import Main from "./Components/Main/Main";
import { useDispatch } from "react-redux";
import { fetchFilteredConferences } from "./store/postData";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchFilteredConferences());
  }, [dispatch]);

  return (
    <div className="App">
      <Main />
    </div>
  );
}

export default App;
