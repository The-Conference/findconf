import React, { useState, useEffect } from "react";
import { Link, useSearchParams, useParams } from "react-router-dom";
import hearts from "../../assets/follow.svg";
import following from "../../assets/following.svg";
import "./conference.scss";
import { useSelector, useDispatch } from "react-redux";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import LazyLoad from "react-lazyload";
import {
  handleSave,
  handleFollow,
  fetchFilteredConferences,
  paginate,
} from "../../store/postData";
import Filters from "../Filters/Filters";
import { options } from "../../utils/options";
import EmptyResult from "../EmptyResult/EmptyResult";
import EmptyFave from "../EmptyResult/emptyFave";
import { getDatesInRange } from "../../utils/getDatesRange";
import Pagination from "../Pagination/Pagination";
const AllConferences = ({ data, keywords, id }) => {
  const { conferences, isLoading, currentPage, conferencesPerPage } =
    useSelector((state) => state.conferences);
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch();
  const { date } = useParams();
  const { periods } = useParams();
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);

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
      return regexp.test(el.conf_name) || regexp.test(el.themes);
    });
  }
  if (data === "search-results") {
    value = searchParams.get("q");
    let newValue = value
      .trim()
      .split(" ")
      .filter((el) => el.length > 2)
      .join("|");

    let regexp = new RegExp(newValue, "gi");
    match = conferences.filter((el) => {
      return (
        regexp.test(el.org_name) ||
        regexp.test(el.conf_name) ||
        regexp.test(el.themes)
      );
    });
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
    collection1: conferences.filter(
      (el) => el.themes.toLowerCase().indexOf("история".toLowerCase()) !== -1
    ),
    collection2: conferences.filter(
      (el) => el.themes.toLowerCase().indexOf("филология".toLowerCase()) !== -1
    ),

    periods: conferences.filter(
      (el) =>
        range.includes(new Date(el.conf_date_begin).toLocaleDateString()) ||
        range.includes(new Date(el.conf_date_end).toLocaleDateString())
    ),
    prev1: conferences
      .filter(
        (el) => el.themes.toLowerCase().indexOf("история".toLowerCase()) !== -1
      )
      .slice(0, 2),
    prev2: conferences
      .filter(
        (el) =>
          el.themes.toLowerCase().indexOf("филология".toLowerCase()) !== -1
      )
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
    result = types.collection1;
  }
  if (data === "collection2") {
    result = types.collection2;
  }
  if (data === "date") {
    result = types.date;
  }
  if (data === "periods") {
    result = types.periods;
  }
  if (data === "prev1") {
    result = types.prev1;
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

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
    } else {
      setFave([...fave, id]);
    }
  };

  let lastConferenceIndex = currentPage * conferencesPerPage;
  let firstConferenceIndex = lastConferenceIndex - conferencesPerPage;
  let currentConference = result.slice(
    firstConferenceIndex,
    lastConferenceIndex
  );

  useEffect(() => {
    dispatch(handleSave(fave));
  }, [dispatch, fave]);
  useEffect(() => {
    dispatch(fetchFilteredConferences());
  }, [dispatch]);

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
          <p>
            <span className="backarrow">&lt;</span> Все конференции
          </p>
        )}

        {data === "favourites" && (
          <p>
            <span className="backarrow">&lt;</span> Избранное
          </p>
        )}
        {data === "search-results" && (
          <p>
            <span className="backarrow">&lt;</span> Результаты по запросу "
            {value}"
          </p>
        )}
        {data === "collection1" && (
          <p>
            <span className="backarrow">&lt;</span> История
          </p>
        )}
        {data === "collection2" && (
          <p>
            <span className="backarrow">&lt;</span> Филология
          </p>
        )}

        {data === "prev1" && (
          <a href="/collection1">
            {" "}
            <p>
              История <span>&gt;</span>
            </p>
          </a>
        )}
        {data === "prev2" && (
          <a href="/collection2">
            <p>
              {" "}
              Филология <span>&gt;</span>
            </p>
          </a>
        )}
        {data === "prev3" && (
          <a href="/all">
            <p>
              Все конференции <span>&gt;</span>
            </p>
          </a>
        )}
        {data === "prev4" && result.length > 0 && (
          <p>
            Похожие конференции <span>&gt;</span>
          </p>
        )}
        {data === "date" && (
          <p>
            <span className="backarrow">&lt;</span> Конференции на{" "}
            <span>{date}</span>
          </p>
        )}
        {data === "periods" && (
          <p>
            <span className="backarrow">&lt;</span> Конференции
            <span>
              c {newPeriod[0].toLocaleDateString("ru", options).slice(0, -7)}
            </span>{" "}
            <span>
              по {newPeriod[1].toLocaleDateString("ru", options).slice(0, -7)}
            </span>
          </p>
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
        {!isLoading &&
          result.length > 0 &&
          currentConference.map((el) => (
            <div key={el.id} className="conference__block">
              <div className="conference__bg">
                <div className="conference__bg-top">
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
                      <span>Идет регистрация</span>
                    ))}
                  <img
                    title={
                      el.follow === false
                        ? "добавить в избранное"
                        : "удалить из избранного"
                    }
                    src={el.follow === false ? hearts : following}
                    alt="follow"
                    onClick={() => {
                      handleFave(el.id);
                      dispatch(handleFollow(el.id));
                    }}
                    width="25"
                    height="24"
                  />
                </div>
                <div className="conference__bg-bottom">
                  {el.conf_date_end === null && el.conf_date_begin === null
                    ? "дата уточняется"
                    : el.conf_date_end !== null
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
                <Link
                  aria-label="Подробнее о конференции"
                  style={{
                    position: "absolute",
                    bottom: "0",
                    left: "0",
                    right: "50px",
                    top: "0",
                  }}
                  to={`/conferences/${el.id}`}
                ></Link>
                <Link
                  aria-label="Подробнее о конференции"
                  style={{
                    position: "absolute",
                    bottom: "0",
                    left: "0",
                    right: "0",
                    top: "50px",
                  }}
                  to={`/conferences/${el.id}`}
                ></Link>
              </div>

              <div className="conference__tags">
                <div>
                  {el.themes.split(",").map((tag, index) => (
                    <small key={index}>{tag}</small>
                  ))}
                </div>
                <Link to={`/conferences/${el.id}`}>
                  <div className="conference__title">{el.conf_name}</div>
                </Link>
              </div>
            </div>
          ))}
      </div>
      {data !== "prev1" &&
        data !== "prev2" &&
        data !== "prev3" &&
        data !== "prev4" &&
        result.length > 20 && (
          <Pagination
            conferencesPerPage={conferencesPerPage}
            totalConferences={result.length}
            paginate={paginate}
          />
        )}
    </section>
  );
};

export default AllConferences;
