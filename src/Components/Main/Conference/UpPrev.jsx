import React from "react";
import "./conference.scss";
import heart from "./follow.svg";

const UpPrev = ({ card, setCard }) => {
  let past = card.filter(
    (item) => new Date(item.date).getMonth() + 1 >= new Date().getMonth() + 1
  );
  let upPrev = past.filter((el, index) => index < 2);

  return (
    <section className="conference">
      <p className="conference__type">
        Предстоящие конференции <span>&gt;</span>
      </p>
      <div className="conference__container">
        {upPrev.map((el) => (
          <div
            el={el.id}
            className="conference__block"
            style={{ opacity: el.finished === true ? "0.5" : "1" }}
          >
            <div className="conference__bg">
              {(el.register === false && (
                <span
                  style={{
                    backgroundColor:
                      el.register === false ? "#939393" : "#37D175",
                  }}
                >
                  Регистрация закончена
                </span>
              )) || <span>Открыта регистрация</span>}
              <img src={heart} alt="follow" />
            </div>
            <div className="conference__tags">
              {el.tags.map((tag) => (
                <small>{tag}</small>
              ))}

              <div className="conference__title">{el.title}</div>
              <div className="conference__organizer">
                <p>Организатор:</p>
                {el.organizer}
              </div>
              <div className="conference__date">
                <p>Дата проведения:</p>
                {el.date}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
export default UpPrev;
