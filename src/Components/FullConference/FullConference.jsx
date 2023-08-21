import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NotFound from "../404/404";
import { filteredContent, hasError, fetchOne } from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { options } from "../../utils/options";
import AllConferences from "../Conference/AllConferences";
import DOMPurify from "dompurify";
import axios from "axios";
import ShareButton from "../ShareButton/ShareButton";
import FollowButton from "../FollowButton/FollowButton";
const FullConference = () => {
  const { confId } = useParams();
  const { conferences, oneConference } = useSelector(
    (state) => state.conferences
  );

  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);

  let content;
  let full = oneConference;
  useEffect(() => {
    const fetchOneConference = async () => {
      const Token = localStorage.getItem("auth_token"); // Получение токена из Local Storage

      const headers = {
        Authorization: `Token ${Token}`,
        Accept: "application/json",
      };

      try {
        if (Token) {
          await axios
            .get(`https://test.theconf.ru/api/${confId}/`, { headers })
            .then((response) => dispatch(fetchOne(response.data)));
        } else {
          await axios
            .get(`https://test.theconf.ru/api/${confId}/`)
            .then((response) => dispatch(fetchOne(response.data)));
        }
      } catch (e) {
        dispatch(hasError(e.message));
      }
    };

    fetchOneConference();
    dispatch(filteredContent());
    window.scrollTo(0, 0);
  }, [confId, dispatch]);

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
  if (oneConference) {
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
            {full.conf_status}
          </span>
          <div className="social">
            <FollowButton
              id={full.id}
              favorite={full.is_favorite}
              type={"full"}
            />

            <ShareButton />
          </div>
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
                (full.reg_date_begin === full.reg_date_end && (
                  <span className="online">
                    {new Date(full.reg_date_end)
                      .toLocaleDateString("ru", options)
                      .slice(0, -3)}
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
              <span>Организатор:</span> {full.un_name}
            </div>
            <hr />
            <div>
              <span>Тематика:</span>{" "}
              <span className="online"> {full.tags.map((el) => el.name)}</span>
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
            {(full.conf_desc !== null && full.conf_desc.length === 0 && (
              <a href={full.conf_card_href} rel="noreferrer" target="_blank">
                Подробнее о конференции
              </a>
            )) ||
              (full.conf_card_href !== null &&
                full.conf_card_href.length > 0 && (
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

  return (
    <>
      <div className="full-conference">{content}</div>
      {full && (
        <div style={{ paddingBottom: "30px" }}>
          <AllConferences data={"prev4"} keywords={full.themes} id={full.id} />
        </div>
      )}
    </>
  );
};
export default FullConference;
