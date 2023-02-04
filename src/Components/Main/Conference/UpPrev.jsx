import React from "react";
import "./conference.scss";
import heart from "./follow.svg";
import following from "./following.svg";

const UpPrev = ({ card, setCard, handleFollow }) => {
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
          <div el={el.id} className="conference__block">
            <div className="conference__bg">
              {(el.register === false && el.finished === false && (
                <span
                  style={{
                    backgroundColor: "#939393",
                  }}
                >
                  Регистрация закончена
                </span>
              )) ||
                (el.register === false && el.finished === true && (
                  <span
                    style={{
                      backgroundColor: "#939393",
                    }}
                  >
                    Конференция завершена
                  </span>
                )) ||
                (el.register === true && el.finished === false && (
                  <span>Открыта регистрация</span>
                ))}
              <img
                src={el.follow === false ? heart : following}
                alt="follow"
                onClick={() => handleFollow(el.id)}
              />
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
