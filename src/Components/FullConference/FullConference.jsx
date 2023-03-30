import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NotFound from "../404/404";
import {
  handleSave,
  handleFollow,
  fetchFilteredConferences,
} from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import follow from "../../assets/followSmall.svg";
import following from "../../assets/followingSmall.svg";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { options } from "../../utils/options";
import AllConferences from "../Conference/AllConferences";
import DOMPurify from "dompurify";
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
          <span
            className={
              full.conf_status === "Ожидается регистрация" ||
              full.conf_status === "Регистрация скоро начнётся" ||
              full.conf_status === "Регистрация началась" ||
              full.conf_status === "Регистрация идёт" ||
              full.conf_status === "Регистрация окончена"
                ? "yellow-status"
                : full.conf_status === "Конференция запланирована" ||
                  full.conf_status === "Конференция скоро начнётся" ||
                  full.conf_status === "Конференция идёт"
                ? "green-status"
                : full.conf_status === "Конференция приостановлена"
                ? "orange-status"
                : full.conf_status === "Конференция окончена"
                ? "grey-status"
                : "red-status"
            }
          >
            {full.conf_status || "Статус уточняется"}
          </span>
          <img
            title={
              full.follow === false
                ? "добавить в избранное"
                : "удалить из избранного"
            }
            src={full.follow === false ? follow : following}
            alt="follow"
            onClick={() => {
              handleFave(full.id);
              dispatch(handleFollow(full.id));
            }}
            width="32"
            height="32"
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
              {full.conf_date_end === null
                ? new Date(full.conf_date_begin)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)
                : full.conf_date_begin === null
                ? new Date(full.conf_date_end)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)
                : full.conf_date_end !== full.conf_date_begin
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
              {full.reg_date_begin === null && full.reg_date_end === null && (
                <span className="online">дата уточняется</span>
              )}
              {(full.reg_date_begin === null && full.reg_date_end !== null && (
                <span className="online">
                  {" "}
                  до{" "}
                  {new Date(full.reg_date_end)
                    .toLocaleDateString("ru", options)
                    .slice(0, -3)}{" "}
                </span>
              )) ||
                (full.reg_date_begin !== null && full.reg_date_end !== null && (
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
                ))}
            </div>
            <div>
              <span>Публикация:</span>
              <span className="online">
                {full.rinc ? "РИНЦ" : "без публикации"}
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
            className={!desc ? "button-passive" : "button-active"}
            onClick={handleDesc}
          >
            Описание
          </button>
          <button
            className={!contacts ? "button-passive" : "button-active"}
            onClick={handleContacts}
          >
            Контакты
          </button>
        </div>

        {desc && !contacts && (
          <div className="full-conference__desc">
            <h1>Условия участия</h1>
            {(full.conf_desc.length === 0 && (
              <a href={full.conf_card_href} rel="noreferrer" target="_blank">
                Подробнее о конференции
              </a>
            )) ||
              (full.conf_card_href.length > 0 && (
                <pre>
                  <div
                    className="full-conference__desc-parsed"
                    dangerouslySetInnerHTML={{
                      __html: DOMPurify.sanitize(full.conf_desc),
                    }}
                  />

                  <div>
                    <a
                      href={full.conf_card_href}
                      rel="noreferrer"
                      target="_blank"
                    >
                      Подробнее о конференции
                    </a>
                  </div>
                </pre>
              ))}
          </div>
        )}
        {!desc && contacts && (
          <div className="full-conference__contacts">
            <pre>
              <div>
                <span>Адрес </span>
                <br /> <p>{full.conf_address}</p>
              </div>
              <div>
                <span>Контактная информация </span>
                <br /> <p>{full.contacts}</p>
              </div>
              <div>
                <p className="useful-links">Полезные ссылки </p>
                <br />
                {full.conf_card_href && (
                  <a
                    rel="noreferrer"
                    target="_blank"
                    href={full.conf_card_href}
                  >
                    Ссылка на источник
                  </a>
                )}
                <br />
                {full.reg_href && (
                  <a rel="noreferrer" target="_blank" href={full.reg_href}>
                    Регистрация
                  </a>
                )}
              </div>
            </pre>
          </div>
        )}
      </div>
    );
  } else if (conferences.length && !full) {
    content = <NotFound />;
  }
  useEffect(() => {
    dispatch(fetchFilteredConferences());
    window.scrollTo(0, 0);
    dispatch(handleSave(fave));
  }, [confId, dispatch, fave]);

  return (
    <>
      <div className="full-conference">{content}</div>
      {full && (
        <div>
          <AllConferences data={"prev4"} keywords={full.themes} id={full.id} />
        </div>
      )}
    </>
  );
};
export default FullConference;
