import React, { useEffect } from "react";

import "./conference.scss";
import FollowButton from "../FollowButton/FollowButton";
import { useSelector, useDispatch } from "react-redux";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import {
  filteredContent,
  handlePage,
  fetchFavourite,
} from "../../store/postData";
import Filters from "../Filters/Filters";
import { options } from "../../utils/options";
import EmptyResult from "../EmptyResult/EmptyResult";
import EmptyFave from "../EmptyResult/emptyFave";

const AllConferences = ({ data, keywords, id }) => {
  const { conferences, isLoading, count, page } = useSelector(
    (state) => state.conferences
  );

  const { value } = useSelector((state) => state.search);
  const dispatch = useDispatch();

  useEffect(() => {
    if (data === "favourites") {
      dispatch(fetchFavourite());
    }
  }, [dispatch, data]);
  useEffect(() => {
    if (
      conferences.length < count &&
      data !== "prev" &&
      data !== "prev4" &&
      data !== "favorites"
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

  const types = {
    prev4: recsPrev.filter((el) => el.id !== id).slice(0, 2),
  };

  if (data === "prev4") {
    result = types.prev4;
  } else {
    result = conferences;
  }

  return (
    <section className={data === "prev4" ? "conf-prev prev" : "conference"}>
      {/* <LoaderTemplateTwo /> */}
      <div className="conference__type">
        {data === "all" && (
          <div className="back">
            <a href="/">
              <span className="backarrow">&lt;</span> <p>Конференции</p>
            </a>
          </div>
        )}

        {data === "favourites" && (
          <div className="back">
            <a href="/">
              <span className="backarrow">&lt;</span> <p>Избранное</p>
            </a>
          </div>
        )}
        {data === "search-results" && (
          <div className="back">
            <span className="backarrow">&lt;</span>{" "}
            <p>Результаты по запросу "{value}"</p>
          </div>
        )}

        {data === "prev4" && result.length > 0 && (
          <div className="similar">
            <p className="forward">Похожие конференции</p>
            <span>&gt;</span>
          </div>
        )}
      </div>
      {data !== "prev" && data !== "prev4" && data !== "favourites" && (
        <Filters />
      )}

      {(isLoading && data !== "prev" && data !== "prev4" && (
        <LoaderTemplate />
      )) ||
        (isLoading && <LoaderTemplateTwo />)}
      {!isLoading &&
        result.length === 0 &&
        data !== "favourites" &&
        data !== "prev" &&
        data !== "prev4" && <EmptyResult />}
      {!isLoading && result.length === 0 && data === "favourites" && (
        <EmptyFave />
      )}
      <div className="conference__container">
        {result.length > 0 &&
          result.map((el) => (
            <div key={el.id} className="conference__block">
              <div className="conference__wrapper">
                <div className="conference__tags">
                  <div className="conference__tags-name">
                    {el.tags.map((elem) =>
                      elem.name
                        .split(",")
                        .map((tag, index) => <span key={index}>{tag}</span>)
                    )}
                    {el.online === true && <span>Онлайн</span>}
                    {el.offline === true && <span>Офлайн</span>}
                    <span>{el.conf_status}</span>
                  </div>
                  <FollowButton
                    id={el.id}
                    favorite={el.is_favorite}
                    type={"card"}
                  />
                </div>
                <h2 className="conference__title">{el.conf_name}</h2>
                <p className="conference__text">
                  Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                  Explicabo suscipit temporibus nihil illum nisi error
                  accusantium, numquam eius nobis excepturi quod iste ex, dicta
                  magnam omnis quis ea molestiae quas. Lorem ipsum dolor sit
                  amet consectetur, adipisicing elit. Explicabo suscipit
                  temporibus nihil illum nisi error accusantium, numquam eius
                  nobis excepturi quod iste ex, dicta magnam omnis quis ea
                  molestiae quas. Lorem ipsum dolor sit amet consectetur,
                  adipisicing elit. Explicabo suscipit temporibus nihil illum
                  nisi error accusantium, numquam eius nobis excepturi quod iste
                  ex, dicta magnam omnis quis ea molestiae quas.
                </p>
                <a
                  className="conference__more"
                  aria-label="Подробнее о конференции"
                  href={`/conferences/${el.id}`}
                >
                  <span></span>
                </a>
                <a
                  className="conference__more2"
                  aria-label="Подробнее о конференции"
                  href={`/conferences/${el.id}`}
                >
                  <span></span>
                </a>
                <div className="conference__date">
                  Дата проведения:
                  <span>
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
                  </span>
                </div>
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
