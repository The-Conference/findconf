import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Filters from "../Filters/Filters";
import {
  handleFollow,
  fetchFilteredConferences,
  handleSave,
} from "../../store/postData";
import { useSelector, useDispatch } from "react-redux";
import following from "../../assets/following.svg";
import hearts from "../../assets/follow.svg";
import { options } from "../../utils/options";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import Calendar from "../Calendar/Calendar";
import EmptyResult from "../EmptyResult/EmptyResult";

const SearchDate = () => {
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);
  const { date } = useParams();
  const dispatch = useDispatch();
  const { conferences, isLoading } = useSelector((state) => state.conferences);

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
    } else {
      setFave([...fave, id]);
    }
  };
  function getDatesInRange(startDate, endDate) {
    const date = new Date(startDate.getTime());
    date.setDate(date.getDate() + 1);
    const dates = [startDate, endDate];
    while (date < endDate) {
      dates.push(new Date(date));
      date.setDate(date.getDate() + 1);
    }
    return dates.map((el) => el.toLocaleDateString());
  }

  let period = conferences.map((el) => {
    const d1 = new Date(el.conf_date_begin);
    const d2 = new Date(el.conf_date_end);
    const id = el.id;
    let period = getDatesInRange(d1, d2);
    return { per: period, ind: id };
  });
  let amount = period.filter((el) => el.per.includes(date));
  let confs = amount.map((el) => el.ind);
  let match = conferences.filter((el) => confs.includes(el.id));

  useEffect(() => {
    dispatch(fetchFilteredConferences());
    window.scrollTo(0, 0);
  }, []);
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
  return (
    <section className="conference">
      {/* <Calendar /> */}
      <p className="conference__type">
        Найдено конференций:<span>{match.length} </span>
      </p>

      <Filters />
      {/* <InfiniteScroll
        dataLength={postData.length} //This is important field to render the next data
        next={fetchData}
        hasMore={hasMore}
        loader={<Spinner />}
      > */}
      {!isLoading &&
        conferences.filter((el) => confs.includes(el.id)).length === 0 && (
          <EmptyResult />
        )}
      {isLoading && <LoaderTemplate />}
      <div className="conference__container">
        {!isLoading &&
          conferences.length > 0 &&
          conferences
            .filter((el) => confs.includes(el.id))
            .map((el) => (
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
                        <span>Открыта регистрация</span>
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
                    />
                  </div>
                  <div
                    className="conference__bg-bottom"
                    style={{
                      maxWidth: el.conf_date_end.length ? "250px" : "140px",
                    }}
                  >
                    {!el.conf_date_end.length && !el.conf_date_begin.length
                      ? "дата уточняется"
                      : el.conf_date_end.length
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
                    style={{
                      position: "absolute",
                      bottom: "0",
                      left: "50px",
                      right: "0",
                      top: "0",
                    }}
                    to={`/conferences/${el.id}`}
                  ></Link>
                  <Link
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
      {/* </InfiniteScroll> */}
    </section>
  );
};
export default SearchDate;
