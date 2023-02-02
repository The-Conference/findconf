import "./App.css";
import Main from "./Components/Main/Main";
import { useState } from "react";
import conferenceCard from "./utils/mock";
import Footer from "./Components/Footer/Footer";
import Header from "./Components/Header/Header";

function App() {
  const [card, setCard] = useState(conferenceCard);
  const handleFollow = (id) => {
    setCard(
      card.map((el) => (el.id === id ? { ...el, follow: !el.follow } : el))
    );
  };
  return (
    <div className="App">
      <Header />
      <Main card={card} setCard={setCard} handleFollow={handleFollow} />
      <Footer />
    </div>
  );
}

export default App;
