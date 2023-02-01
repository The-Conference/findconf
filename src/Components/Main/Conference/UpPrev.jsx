import React from "react";

const UpPrev = ({ card, setCard }) => {
  let past = card.filter(
    (item) => new Date(item.date).getMonth() + 1 >= new Date().getMonth() + 1
  );
  let upPrev = past.filter((el, index) => index < 2);

  return (
    <section>
      <p>Предстоящие конференции</p>
      {upPrev.map((el) => (
        <div el={el.id}>
          <div>{el.title}</div>
          <div>{el.date}</div>
        </div>
      ))}
    </section>
  );
};
export default UpPrev;
