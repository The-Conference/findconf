import "./App.css";
import React, { useEffect } from "react";
import Main from "./Components/Main/Main";
import { useDispatch } from "react-redux";
import { fetchOnce } from "./store/postData";

function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchOnce());
  }, [dispatch]);

  return (
    <div className="App">
      <Main />
    </div>
  );
}

export default App;
