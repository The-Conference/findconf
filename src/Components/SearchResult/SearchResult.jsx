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

const SearchResult = () => {
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);
  const { value } = useParams();
  const dispatch = useDispatch();
  const { conferences, isLoading } = useSelector((state) => state.conferences);

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
    } else {
      setFave([...fave, id]);
    }
  };
  let match = conferences.filter((el) => {
    return (
      el.org_name.toLowerCase().indexOf(value.toLowerCase()) !== -1 ||
      el.conf_name.toLowerCase().indexOf(value.toLowerCase()) !== -1 ||
      el.themes.toLowerCase().indexOf(value.toLowerCase()) !== -1
    );
  });

  useEffect(() => {
    dispatch(fetchFilteredConferences());
    window.scrollTo(0, 0);
  }, []);
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
  return (
    <section className="conference">
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
      {isLoading && <LoaderTemplate />}
      <div className="conference__container">
        {!isLoading && match.length === 0 && (
          <div style={{ minHeight: "100vh" }}>
            <p>По запросу {value} ничего не найдено. </p>

            <p>Рекомендации:</p>

            <p>Убедитесь, что все слова написаны без ошибок.</p>
            <p>Попробуйте использовать другие ключевые слова.</p>
            <p>Попробуйте использовать более популярные ключевые слова.</p>
            <p>Попробуйте уменьшить количество слов в запросе.</p>
          </div>
        )}
        {match.length > 0 &&
          match.map((el) => (
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
export default SearchResult;
