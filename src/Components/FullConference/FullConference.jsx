import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NotFound from "../404/404";
import {
  fetchAllConferences,
  handleSave,
  handleFollow,
} from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import follow from "../../assets/followSmall.svg";
import following from "../../assets/followingSmall.svg";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { options } from "../../utils/options";

const FullConference = () => {
  const { confId } = useParams();
  const { conferences } = useSelector((state) => state.conferences);
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);
  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);
  let content;
  let full = conferences.find(({ id }) => id === +confId);

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
      console.log(fave);
    } else {
      setFave([...fave, id]);
    }
  };

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
          <h1>{full.conf_name}</h1>
          <small>Информация актуальна на {full.conf_date_begin} </small>
        </div>

        <div className="full-conference__card">
          <div className="full-conference__card-flex">
            <div>
              <span>Дата проведения:</span>
              {!full.conf_date_end.length && !full.conf_date_begin.length
                ? "дата уточняется"
                : full.conf_date_end.length
                ? new Date(full.conf_date_begin)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3) +
                  " - " +
                  new Date(full.conf_date_end)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)
                : new Date(full.conf_date_begin)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
            </div>
            <div>
              <span>Форма участия:</span>
              <span className="both">
                {full.online ? "онлайн" : ""} {full.offline ? "оффлайн" : ""}
              </span>
            </div>
            <div>
              <span>Регистрация:</span>
              {(full.reg_date_begin.length === 0 &&
                full.reg_date_end.length !== 0 && (
                  <span className="online">
                    {" "}
                    до{" "}
                    {new Date(full.reg_date_end)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}{" "}
                  </span>
                )) || (
                <span className="online">
                  {" "}
                  {new Date(full.reg_date_begin)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
                  -
                  {new Date(full.reg_date_end)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}
                </span>
              )}
            </div>
            <div>
              <span>Публикация:</span>
              <span className="online">
                {full.rinc ? "ринц" : "без публикации"}
              </span>
            </div>
          </div>
          <hr />
          <div className="full-conference__card-block">
            <div>
              <span>Организатор:</span> {full.org_name}
            </div>
            <hr />
            <div>
              <span>Тематика:</span>{" "}
              <span className="online"> {full.themes}</span>
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
            {(full.conf_desc.length === 0 && (
              <a href={full.conf_card_href} rel="noreferrer" target="_blank">
                Подробнее о конференции
              </a>
            )) || (
              <div>
                {full.conf_desc}
                <div>
                  <a
                    href={full.conf_card_href}
                    rel="noreferrer"
                    target="_blank"
                  >
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
              <br /> {full.conf_address}
            </div>
            <div>
              <span>Контактная информация </span>
              <br /> <span className="details">{full.contacts}</span>
            </div>
            <div>
              <span>Полезные ссылки </span>
              <br />
              <a rel="noreferrer" target="_blank" href={full.conf_card_href}>
                Ссылка на источник
              </a>{" "}
              <br />
              {full.reg_href.length > 0 && (
                <a rel="noreferrer" target="_blank" href={full.reg_href}>
                  Регистрация
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    );
  } else if (conferences.length && !full) {
    content = <NotFound />;
  }
  useEffect(() => {
    dispatch(fetchAllConferences());
    window.scrollTo(0, 0);
  }, [confId]);
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
  return <div className="full-conference">{content}</div>;
};
export default FullConference;
