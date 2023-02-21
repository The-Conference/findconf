import "./App.css";
import React from "react";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import Main from "./Components/Main/Main";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchAllConferences } from "./store/postData";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchAllConferences());
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
