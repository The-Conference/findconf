import "./App.css";
import Main from "./Components/Main/Main";
import { useState } from "react";
import conferenceCard from "./utils/mock";
function App() {
  const [card, setCard] = useState(conferenceCard);
  return (
    <div className="App">
      <Main card={card} setCard={setCard} />
    </div>
  );
}

export default App;
