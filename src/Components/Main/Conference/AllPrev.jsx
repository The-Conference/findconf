import React from "react";

const AllPrev = ({ card, setCard }) => {
  let preview = card.filter((item, index) => index < 2);

  return (
    <section>
      <p>Все конференции</p>
      {preview.map((el) => (
        <div key={el.id}>
          <div>{el.title}</div>
          <div>{el.date}</div>
        </div>
      ))}
    </section>
  );
};
export default AllPrev;
