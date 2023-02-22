import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchAllConferences } from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import follow from "./follow.svg";
const FullConference = () => {
  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);
  const { conferences } = useSelector((state) => state.conferences);
  const { itemId } = useParams();
  let conf = 0;
  let full = conferences.find(({ id }) => id === itemId);
  if (full) {
    conf = full;
  }
  var options = { year: "numeric", month: "long", day: "numeric" };
  console.log(conferences);
  useEffect(() => {
    dispatch(fetchAllConferences());
    window.scrollTo(0, 0);
  }, []);

  const handleDesc = () => {
    if (contacts === true) {
      setContacts(false);
      setDesc(true);
    }
  };
  const handleContacts = () => {
    if (desc === true) setDesc(false);
    setContacts(true);
  };

  return (
    <div className="full-conference">
      {(conf === 0 && <div style={{ height: "100vh" }}>404</div>) || (
        <div className="full-conference__container">
          <div className="full-conference__container-top">
            <span>Открыта регистрация</span>
            <img src={follow} alt="сохранить" />
          </div>

          <div className="full-conference__title">
            <h1>{conf.title}</h1>
            <small>Информация актуальна на {conf.dateStart} </small>
          </div>

          <div className="full-conference__card">
            <div className="full-conference__card-flex">
              <div>
                <span>Дата проведения:</span>
                {!conf.dateEnd.length && !conf.dateStart.length
                  ? "дата уточняется"
                  : conf.dateEnd.length
                  ? new Date(conf.dateStart)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3) +
                    " - " +
                    new Date(conf.dateEnd)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)
                  : new Date(conf.dateStart)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}
              </div>
              <div>
                <span>Форма участия:</span>
                {(conf.online === true && conf.offline === true && (
                  <span className="both">online, offline</span>
                )) ||
                  (conf.offline === true && (
                    <span className="offline">offline</span>
                  )) ||
                  (conf.online === true && (
                    <span className="online">online</span>
                  ))}
              </div>
              <div>
                <span>Регистрация:</span>{" "}
              </div>
              <div>
                <span>Публикация:</span>Ринц, Вак
              </div>
            </div>
            <hr />
            <div className="full-conference__card-block">
              <div>
                <span>Организатор:</span> {conf.organizer}
              </div>
              <hr />
              <div>
                <span>Тематика:</span>
              </div>
            </div>
          </div>
          <div className="full-conference__tabs">
            <button
              style={{
                color: !desc ? "#2C60E7" : "white",
                backgroundColor: !desc ? "#EBEFFF" : "#2C60E7",
              }}
              onClick={handleDesc}
            >
              Описание
            </button>
            <button
              style={{
                color: !contacts ? "#2C60E7" : "white",
                backgroundColor: !contacts ? "#EBEFFF" : "#2C60E7",
              }}
              onClick={handleContacts}
            >
              Контакты
            </button>
          </div>

          {desc && !contacts && (
            <div className="full-conference__desc">
              <h3>Дополнительная информация</h3>
              {(conf.description.length === 0 && (
                <a href={conf.link} rel="noreferrer" target="_blank">
                  Подробнее о конференции
                </a>
              )) || (
                <div>
                  {conf.description}{" "}
                  <div>
                    <a href={conf.link} rel="noreferrer" target="_blank">
                      Подробнее о конференции
                    </a>
                  </div>
                </div>
              )}
            </div>
          )}
          {!desc && contacts && (
            <div className="full-conference__contacts">
              <div>
                <span>Адрес </span>
                <br /> {conf.address}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
export default FullConference;
