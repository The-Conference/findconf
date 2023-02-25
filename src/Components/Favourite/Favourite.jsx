import React from "react";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllConferences } from "../../store/postData";
import "../Main/Conference/conference.scss";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import hearts from "./follow.svg";
import following from "./following.svg";
import { Link } from "react-router-dom";
import { handleFollow, handleSave } from "../../store/postData";

const Favourites = () => {
  const dispatch = useDispatch();
  const { conferences } = useSelector((state) => state.conferences);
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
  useEffect(() => {
    dispatch(handleSave(fave));
    dispatch(fetchAllConferences());
  }, [fave]);

  var options = { year: "numeric", month: "long", day: "numeric" };

  return (
    <section className="conference">
      <a href="/all">
        <p className="conference__type">
          Избранное <span>&gt;</span>
        </p>
      </a>
      {/* <InfiniteScroll
        dataLength={postData.length}
        next={fetchData}
        hasMore={hasMore}
        loader={<LoaderTemplate />}
      > */}
      <div className="conference__container">
        {conferences
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
                    title="добавить в избранное"
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
                  style={{ maxWidth: el.dateEnd.length ? "250px" : "140px" }}
                >
                  {!el.dateEnd.length && !el.dateStart.length
                    ? "дата уточняется"
                    : el.dateEnd.length
                    ? new Date(el.dateStart)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3) +
                      " - " +
                      new Date(el.dateEnd)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)
                    : new Date(el.dateStart)
                        .toLocaleDateString("ru", options)
                        .slice(0, -3)}
                </div>
              </div>

              <div className="conference__tags">
                {/* <div>
                  {el.tags.map((tag) => (
                    <small>{tag}</small>
                  ))}
                </div> */}
                <Link to={`/conferences/${el.id}`}>
                  <div className="conference__title">{el.title}</div>
                </Link>
              </div>
            </div>
          ))}
        {conferences.filter((el) => el.follow === true).length === 0 && (
          <div>Добавьте интересные конференции в избранное</div>
        )}
      </div>
      {/* </InfiniteScroll> */}
    </section>
  );
};

export default Favourites;
