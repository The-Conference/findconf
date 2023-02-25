import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchAllConferences } from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import follow from "./follow.svg";
import following from "./following.svg";
import { handleSave, handleFollow } from "../../store/postData";
const FullConference = () => {
  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);
  const { conferences } = useSelector((state) => state.conferences);
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
      console.log(fave);
    } else {
      setFave([...fave, id]);
    }
  };
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
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
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
            <img
              title="добавить в избранное"
              src={conf.follow === false ? follow : following}
              alt="follow"
              onClick={() => {
                handleFave(conf.id);
                dispatch(handleFollow(conf.id));
              }}
            />
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
                <span>Регистрация:</span>
                {(conf.regStart.length === 0 && conf.regEnd.length !== 0 && (
                  <span className="online">
                    {" "}
                    до{" "}
                    {new Date(conf.regEnd)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}{" "}
                  </span>
                )) || (
                  <span className="online">
                    {" "}
                    {new Date(conf.regStart)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}
                    -
                    {new Date(conf.regEnd)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}
                  </span>
                )}
              </div>
              <div>
                <span>Публикация:</span>{" "}
                {conf.rinc === true && <span className="online">ринц</span>}
              </div>
            </div>
            <hr />
            <div className="full-conference__card-block">
              <div>
                <span>Организатор:</span> {conf.organizer}
              </div>
              <hr />
              <div>
                <span>Тематика:</span>{" "}
                <span className="online"> {conf.tags}</span>
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
              <h3>Условия участия</h3>
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
              <div>
                <span>Контактная информация </span>
                <br /> <span className="details">{conf.contacts}</span>
              </div>
              <div>
                <span>Полезные ссылки </span>
                <br />
                <a href={conf.link}>Ссылка на источник</a> <br />
                {conf.reg.length > 0 && <a href={conf.link}>Регистрация</a>}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
export default FullConference;
