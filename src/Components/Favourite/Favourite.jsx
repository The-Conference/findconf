import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchFilteredConferences,
  handleFollow,
  handleSave,
} from "../../store/postData";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import Filters from "../Filters/Filters";
import hearts from "../../assets/follow.svg";
import following from "../../assets/following.svg";
import { Link } from "react-router-dom";
import { options } from "../../utils/options";
import EmptyFave from "../EmptyResult/emptyFave";

const Favourites = () => {
  const dispatch = useDispatch();
  const { conferences, isLoading } = useSelector((state) => state.conferences);
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
    } else {
      setFave([...fave, id]);
    }
  };
  useEffect(() => {
    dispatch(handleSave(fave));
    dispatch(fetchFilteredConferences());
  }, []);

  return (
    <section className="conference">
      <p className="conference__type">
        Избранное <span>&gt;</span>
      </p>
      <Filters />
      {/* <InfiniteScroll
        dataLength={postData.length}
        next={fetchData}
        hasMore={hasMore}
        loader={<LoaderTemplate />}
      > */}
      {!isLoading &&
        conferences.filter((el) => el.follow === true).length === 0 && (
          <EmptyFave />
        )}
      {isLoading && <LoaderTemplate />}

      <div className="conference__container">
        {!isLoading &&
          conferences
            .filter((el) => el.follow === true)
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

export default Favourites;
