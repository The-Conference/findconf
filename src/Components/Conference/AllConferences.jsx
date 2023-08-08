import React, { useEffect } from "react";
import { Link, useSearchParams, useParams } from "react-router-dom";
import hearts from "../../assets/follow.svg";
// import following from "../../assets/following.svg";
import "./conference.scss";

import { useSelector, useDispatch } from "react-redux";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import { filteredContent, handlePage } from "../../store/postData";
import Filters from "../Filters/Filters";
import { options } from "../../utils/options";
import EmptyResult from "../EmptyResult/EmptyResult";
import EmptyFave from "../EmptyResult/emptyFave";
import { getDatesInRange } from "../../utils/getDatesRange";

const AllConferences = ({ data, keywords, id }) => {
  const { conferences, isLoading, count, page } = useSelector(
    (state) => state.conferences
  );
  const [searchParams] = useSearchParams();

  const dispatch = useDispatch();
  const { periods, date } = useParams();

  useEffect(() => {
    if (
      conferences.length < count &&
      data !== "prev4" &&
      data !== "prev3" &&
      data !== "prev2" &&
      data !== "prev1"
    ) {
      const fetchData = async () => {
        try {
          dispatch(handlePage(page + 1));

          dispatch(filteredContent());
        } catch (error) {
          console.log(error);
        }
      };

      const handleScroll = () => {
        const scrollHeight = document.documentElement.scrollHeight;
        const scrollTop = document.documentElement.scrollTop;
        const clientHeight = document.documentElement.clientHeight;

        // проверяем, достигли ли мы конца скролла
        if (scrollTop + clientHeight + 100 >= scrollHeight && !isLoading) {
          fetchData();
        }
      };

      window.addEventListener("scroll", handleScroll);
      return () => {
        window.removeEventListener("scroll", handleScroll);
      };
    }
  }, [dispatch, isLoading, page, count, conferences.length, data]);

  let result = [];
  let match = [];
  let confs = [];
  let range = [];
  let value = [];
  let newPeriod = [];
  let recsPrev = [];

  if (data === "prev4") {
    let newValue = keywords
      .trim()
      .split(" ")
      .filter((el) => el.length > 2)
      .join("|");

    let regexp = new RegExp(newValue, "gi");
    recsPrev = conferences.filter((el) => {
      return (
        regexp.test(el.conf_name) ||
        regexp.test(el.tags.map((item) => item.name))
      );
    });
  }
  if (data === "search-results") {
    value = searchParams.get("search");
    if (value) {
      let newValue = value
        .trim()
        .split(" ")
        .filter((el) => el.length > 2)
        .join("|");

      let regexp = new RegExp(newValue, "gi");
      match = conferences.filter((el) => {
        return (
          regexp.test(el.un_name) ||
          regexp.test(el.conf_name) ||
          regexp.test(el.tags.map((el) => el.name))
        );
      });
    }
  }
  if (data === "date") {
    let period = conferences.map((el) => {
      const d1 = new Date(el.conf_date_begin);
      const d2 = new Date(el.conf_date_end);
      const id = el.id;
      let period = getDatesInRange(d1, d2);
      return { per: period, ind: id };
    });
    let amount = period.filter((el) => el.per.includes(date));
    confs = amount.map((el) => el.ind);
  }
  if (data === "periods") {
    newPeriod = periods.split(",").map((item) => new Date(item));
    range = getDatesInRange(newPeriod[0], newPeriod[1]);
  }

  const types = {
    all: conferences,
    favourites: conferences.filter((el) => el.follow === true),
    searchRes: match,
    date: conferences.filter((el) => confs.includes(el.id)),

    periods: conferences.filter(
      (el) =>
        range.includes(new Date(el.conf_date_begin).toLocaleDateString()) ||
        range.includes(new Date(el.conf_date_end).toLocaleDateString())
    ),
    // prev1: conferences.slice(0, 2),
    prev2: conferences
      .filter((el) => el.conf_status === "Конференция окончена")
      .slice(0, 2),
    prev3: conferences.slice(0, 2),
    prev4: recsPrev.filter((el) => el.id !== id).slice(0, 2),
  };

  if (data === "all") {
    result = types.all;
  }
  if (data === "favourites") {
    result = types.favourites;
  }
  if (data === "search-results") {
    result = types.searchRes;
  }
  if (data === "collection1") {
    result = conferences;
  }
  if (data === "collection2") {
    result = conferences;
  }
  if (data === "date") {
    result = types.date;
  }
  if (data === "periods") {
    result = types.periods;
  }
  if (data === "prev1") {
    result = conferences.slice(0, 2);
  }
  if (data === "prev2") {
    result = types.prev2;
  }
  if (data === "prev3") {
    result = types.prev3;
  }
  if (data === "prev4") {
    result = types.prev4;
  }

  return (
    <section
      className={
        data === "prev1" ||
        data === "prev2" ||
        data === "prev3" ||
        data === "prev4"
          ? "conference prev preview-bottom"
          : "conference"
      }
    >
      <div className="conference__type">
        {data === "all" && (
          <div className="back">
            <Link to="/">
              <span className="backarrow">&lt;</span> <p>Все конференции</p>
            </Link>
          </div>
        )}

        {data === "favourites" && (
          <div className="back">
            <Link to="/">
              <span className="backarrow">&lt;</span> <p>Избранное</p>
            </Link>
          </div>
        )}
        {data === "search-results" && (
          <div className="back">
            <span className="backarrow">&lt;</span>{" "}
            <p>Результаты по запросу "{value}"</p>
          </div>
        )}
        {data === "collection1" && (
          <div className="back">
            <Link to="/">
              {" "}
              <span className="backarrow">&lt;</span>{" "}
              <p>Предстоящие конференции</p>
            </Link>
          </div>
        )}
        {data === "collection2" && (
          <div className="back">
            <Link to="/">
              <span className="backarrow">&lt;</span>{" "}
              <p>Прошедшие конференции</p>
            </Link>
          </div>
        )}

        {data === "prev1" && (
          <a href="/collection1?conf_status=starting_soon%2C">
            <p className="forward">Предстоящие конференции</p>
            <span>&gt;</span>
          </a>
        )}
        {data === "prev2" && (
          <a href="/collection2?conf_status=finished%2C">
            <p className="forward">Прошедшие конференции</p>
            <span>&gt;</span>
          </a>
        )}
        {data === "prev3" && (
          <a href="/all">
            <p className="forward">Все конференции</p>
            <span>&gt;</span>
          </a>
        )}
        {data === "prev4" && result.length > 0 && (
          <div className="similar">
            <p className="forward">Похожие конференции</p>
            <span>&gt;</span>
          </div>
        )}
        {data === "date" && (
          <div className="back">
            <Link to="/">
              <span className="backarrow">&lt;</span>{" "}
              <p>
                Конференции на <span>{date}</span>
              </p>
            </Link>
          </div>
        )}
        {data === "periods" && (
          <div className="back">
            <Link to="/">
              <span className="backarrow">&lt;</span>{" "}
              <p>
                Конференции c{" "}
                {newPeriod[0].toLocaleDateString("ru", options).slice(0, -7)}
                по {newPeriod[1].toLocaleDateString("ru", options).slice(0, -7)}
              </p>
            </Link>
          </div>
        )}
      </div>
      {data !== "prev1" &&
        data !== "prev2" &&
        data !== "prev3" &&
        data !== "prev4" && <Filters />}

      {(isLoading &&
        data !== "prev1" &&
        data !== "prev2" &&
        data !== "prev3" &&
        data !== "prev4" && <LoaderTemplate />) ||
        (isLoading && <LoaderTemplateTwo />)}
      {!isLoading &&
        result.length === 0 &&
        data !== "favourites" &&
        data !== "prev1" &&
        data !== "prev2" &&
        data !== "prev3" &&
        data !== "prev4" && <EmptyResult />}
      {!isLoading && result.length === 0 && data === "favourites" && (
        <EmptyFave />
      )}
      <div className="conference__container">
        {result.length > 0 &&
          result.map((el) => (
            <div key={el.id} className="conference__block">
              <div className="conference__bg">
                <div className="conference__bg-top">
                  <span
                    className={
                      el.conf_status === "Ожидается регистрация" ||
                      el.conf_status === "Регистрация скоро начнётся" ||
                      el.conf_status === "Регистрация началась" ||
                      el.conf_status === "Регистрация идёт" ||
                      el.conf_status === "Регистрация окончена"
                        ? "yellow-status"
                        : el.conf_status === "Конференция запланирована" ||
                          el.conf_status === "Конференция скоро начнётся" ||
                          el.conf_status === "Конференция идёт"
                        ? "green-status"
                        : el.conf_status === "Конференция приостановлена"
                        ? "orange-status"
                        : el.conf_status === "Конференция окончена"
                        ? "grey-status"
                        : "red-status"
                    }
                  >
                    {el.conf_status}
                  </span>
                  <img
                    title="добавить в избранное"
                    src={hearts}
                    alt="follow"
                    width="25"
                    height="24"
                  />
                </div>
                <div className="conference__bg-middle">
                  {el.tags.map((el) => el.name).length > 0 ? (
                    <div>#{el.tags[0].name}</div>
                  ) : null}
                </div>
                <div className="conference__bg-bottom">
                  {el.conf_date_end === null
                    ? new Date(el.conf_date_begin)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)
                    : el.conf_date_begin === null
                    ? new Date(el.conf_date_end)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)
                    : el.conf_date_end !== el.conf_date_begin
                    ? new Date(el.conf_date_begin)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3) +
                      " - " +
                      new Date(el.conf_date_end)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)
                    : new Date(el.conf_date_begin)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)}
                </div>
                <a
                  aria-label="Подробнее о конференции"
                  style={{
                    position: "absolute",
                    bottom: "0",
                    left: "0",
                    right: "50px",
                    top: "0",
                  }}
                  href={`/conferences/${el.id}`}
                >
                  <span></span>
                </a>
                <a
                  aria-label="Подробнее о конференции"
                  style={{
                    position: "absolute",
                    bottom: "0",
                    left: "0",
                    right: "0",
                    top: "50px",
                  }}
                  href={`/conferences/${el.id}`}
                >
                  <span></span>
                </a>
              </div>

              <div className="conference__tags">
                <div className="conference__tags-container">
                  {el.tags.map((elem) =>
                    elem.name
                      .split(",")
                      .map((tag, index) => <small key={index}>{tag}</small>)
                  )}
                  {el.online === true && <small>онлайн</small>}
                  {el.offline === true && <small>офлайн</small>}
                </div>
                <a href={`/conferences/${el.id}`}>
                  <div className="conference__title">{el.conf_name}</div>
                </a>
              </div>
            </div>
          ))}
      </div>
      {isLoading && (
        <div style={{ marginTop: "50px" }}>
          <LoaderTemplateTwo />
        </div>
      )}
    </section>
  );
};

export default AllConferences;
