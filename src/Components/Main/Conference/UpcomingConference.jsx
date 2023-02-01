import React from "react";

const UpcomingConference = ({ card, setCard }) => {
  return (
    <section>
      <p>Предстоящие конференции</p>
      {card.map(
        (el) =>
          new Date(el.date).getMonth() + 1 >= new Date().getMonth() + 1 &&
          new Date(el.date).getYear() >= new Date().getYear() && (
            <div key={el.id}>
              <div>{el.title}</div> <div>{el.date}</div>
            </div>
          )
      )}
    </section>
  );
};
export default UpcomingConference;
