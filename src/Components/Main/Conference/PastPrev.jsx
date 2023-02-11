import React from "react";
import heart from "./follow.svg";
import following from "./following.svg";

import { handleFollow, card } from "../../../store/postData";
import { useDispatch, useSelector } from "react-redux";

const PastPrev = () => {
  const dispatch = useDispatch();
  const data = useSelector(card);
  let past = data.filter((item) => item.finished === true);
  let pastPrev = past.filter((el, index) => index < 2);

  return (
    <section className="conference">
      <a href="/finished">
        <p className="conference__type">
          Прошедшие конференции <span>&gt;</span>
        </p>
      </a>
      <div className="conference__container">
        {pastPrev.map((el) => (
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
                onClick={() => dispatch(handleFollow(el.id))}
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
export default PastPrev;
