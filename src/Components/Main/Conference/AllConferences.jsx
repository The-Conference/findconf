import React from "react";

const AllConferences = ({ card, setCard }) => {
  return (
    <section>
      <p>Все конференции</p>
      {card.map((el) => (
        <div key={el.id}>
          <div>{el.title}</div> <div>{el.date}</div>
        </div>
      ))}
    </section>
  );
};
export default AllConferences;
