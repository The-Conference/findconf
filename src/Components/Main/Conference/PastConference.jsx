import React from "react";

const PastConference = ({ card, setCard }) => {
  return (
    <section>
      <p>Прошедшие конференции</p>
      {card.map(
        (el) =>
          new Date(el.date).getMonth() + 1 < new Date().getMonth() + 1 && (
            <div key={el.id}>
              <div>{el.title}</div> <div>{el.date}</div>
            </div>
          )
      )}
    </section>
  );
};

export default PastConference;
