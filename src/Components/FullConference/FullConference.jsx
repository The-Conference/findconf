import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NotFound from "../404/404";
import { fetchAllConferences } from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import follow from "./follow.svg";
import following from "./following.svg";
import { handleSave, handleFollow } from "../../store/postData";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";

const FullConference = () => {
  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);
  const { conferences, isLoading } = useSelector((state) => state.conferences);
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
  const { confId } = useParams();

  var options = { year: "numeric", month: "long", day: "numeric" };

  useEffect(() => {
    dispatch(fetchAllConferences());
    window.scrollTo(0, 0);
  }, [confId]);
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

  let full = conferences.find(({ id }) => id === +confId);

  let content;
  if (conferences.length === 0) {
    content = <LoaderTemplate />;
  }
  if (conferences.filter((el) => el.id === +confId).length > 0) {
    content = (
      <div className="full-conference__container">
        <div className="full-conference__container-top">
          <span>Открыта регистрация</span>
          <img
            title="добавить в избранное"
            src={full.follow === false ? follow : following}
            alt="follow"
            onClick={() => {
              handleFave(full.id);
              dispatch(handleFollow(full.id));
            }}
          />
        </div>
        <div className="full-conference__title">
          <h1>{full.title}</h1>
          <small>Информация актуальна на {full.dateStart} </small>
        </div>

        <div className="full-conference__card">
          <div className="full-conference__card-flex">
            <div>
              <span>Дата проведения:</span>
              {!full.dateEnd.length && !full.dateStart.length
                ? "дата уточняется"
                : full.dateEnd.length
                ? new Date(full.dateStart)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3) +
                  " - " +
                  new Date(full.dateEnd)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)
                : new Date(full.dateStart)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
            </div>
            <div>
              <span>Форма участия:</span>
              <span className="both">{full.online + " " + full.offline}</span>
            </div>
            <div>
              <span>Регистрация:</span>
              {(full.regStart.length === 0 && full.regEnd.length !== 0 && (
                <span className="online">
                  {" "}
                  до{" "}
                  {new Date(full.regEnd)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}{" "}
                </span>
              )) || (
                <span className="online">
                  {" "}
                  {new Date(full.regStart)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
                  -
                  {new Date(full.regEnd)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
                </span>
              )}
            </div>
            <div>
              <span>Публикация:</span>
              <span className="online">{full.rinc}</span>
            </div>
          </div>
          <hr />
          <div className="full-conference__card-block">
            <div>
              <span>Организатор:</span> {full.organizer}
            </div>
            <hr />
            <div>
              <span>Тематика:</span>{" "}
              <span className="online"> {full.tags.join(",  ")}</span>
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
            {(full.description.length === 0 && (
              <a href={full.link} rel="noreferrer" target="_blank">
                Подробнее о конференции
              </a>
            )) || (
              <div>
                {full.description}
                <div>
                  <a href={full.link} rel="noreferrer" target="_blank">
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
              <br /> {full.address}
            </div>
            <div>
              <span>Контактная информация </span>
              <br /> <span className="details">{full.contacts}</span>
            </div>
            <div>
              <span>Полезные ссылки </span>
              <br />
              <a href={full.link}>Ссылка на источник</a> <br />
              {full.reg.length > 0 && <a href={full.link}>Регистрация</a>}
            </div>
          </div>
        )}
      </div>
    );
  } else if (conferences.length && !full) {
    content = <NotFound />;
  }

  return <div className="full-conference">{content}</div>;
};
export default FullConference;
