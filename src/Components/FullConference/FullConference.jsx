import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NotFound from "../404/404";
import {
  filteredContent,
  hasError,
  fetchOne,
  startLoading,
} from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import "./fullconference.scss";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import DOMPurify from "dompurify";
import axios from "axios";
import ShareButton from "../ShareButton/ShareButton";
import FollowButton from "../FollowButton/FollowButton";
import { DateFormatter } from "../../utils/options";
const FullConference = () => {
  const { confId } = useParams();
  const { conferences, oneConference, isLoading } = useSelector(
    (state) => state.conferences
  );

  const dispatch = useDispatch();
  const [desc, setDesc] = useState(true);
  const [contacts, setContacts] = useState(false);

  let content;
  let full = oneConference;

  useEffect(() => {
    const fetchOneConference = async () => {
      dispatch(startLoading());
      const Token = localStorage.getItem("auth_token"); // Получение токена из Local Storage

      const headers = {
        Authorization: `Token ${Token}`,
        Accept: "application/json",
      };

      try {
        if (Token) {
          await axios
            .get(`https://test.theconf.ru/api/confs/${confId}/`, { headers })
            .then((response) => dispatch(fetchOne(response.data)));
        } else {
          await axios
            .get(`https://test.theconf.ru/api/confs/${confId}/`)
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
  if (!full && !isLoading && conferences.length > 0) {
    content = <NotFound />;
  }
  if (isLoading) {
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
          <h1>{full.title}</h1>
          <small>Информация актуальна на {full.conf_date_begin} </small>
        </div>

        <div className="full-conference__card">
          <div className="full-conference__card-flex">
            <div>
              <span>Дата проведения:</span>
              {DateFormatter(full)}
            </div>
            <div>
              <span>Форма участия:</span>
              <span className="both">{full.online ? "онлайн" : ""}</span>
              <span className="both">{full.offline ? "оффлайн" : ""}</span>
            </div>
            <div>
              <span>Регистрация:</span>
              {/* {full.reg_date_begin === null && full.reg_date_end === null && (
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
                ))} */}
            </div>
            <div>
              <span>Публикация:</span>
              <span className="online">
                <span className="publish">{full.rinc ? "РИНЦ   " : ""}</span>
                <span className="publish">{full.vak ? "ВАК   " : ""}</span>
                <span className="publish"> {full.wos ? "WOS    " : ""}</span>
                <span className="publish">
                  {!full.scopus &&
                    !full.wos &&
                    !full.vak &&
                    !full.rinc &&
                    "без публикации"}
                </span>
                <span className="publish">
                  {full.scopus ? "Scopus    " : ""}
                </span>
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
              {full.tags.map((el) => (
                <span className="online"> {el.name}</span>
              ))}
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
            {(full.description !== null && full.description.length === 0 && (
              <a href={full.source_href} rel="noreferrer" target="_blank">
                Подробнее о конференции
              </a>
            )) || (
              <pre>
                <div
                  className="full-conference__desc-parsed"
                  dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(full.description),
                  }}
                />

                <div>
                  <a href={full.source_href} rel="noreferrer" target="_blank">
                    Подробнее о конференции
                  </a>
                </div>
              </pre>
            )}
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
                {full.source_href && (
                  <a rel="noreferrer" target="_blank" href={full.source_href}>
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
  }

  return (
    <>
      <div className="full-conference">{content}</div>
    </>
  );
};
export default FullConference;
