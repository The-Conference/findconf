import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
// import Filters from "../Filters/Filters";
import { handleFollow, fetchAllConferences } from "../../store/postData";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import following from "./following.svg";
import hearts from "./follow.svg";
import { handleSave } from "../../store/postData";
const SearchResult = () => {
  const { value } = useParams();
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
  var options = { year: "numeric", month: "long", day: "numeric" };

  let match = conferences.filter((el) => {
    return (
      el.organizer.toLowerCase().indexOf(value.toLowerCase()) !== -1 ||
      el.title.toLowerCase().indexOf(value.toLowerCase()) !== -1
    );
  });

  console.log(match);

  useEffect(() => {
    dispatch(fetchAllConferences());
    window.scrollTo(0, 0);
  }, []);
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
  return (
    <section className="conference">
      <a href="/">
        <p className="conference__type">
          Найдено <span>{match.length} </span>
          конференции
        </p>
      </a>
      {/* <Filters /> */}
      {/* <InfiniteScroll
        dataLength={postData.length} //This is important field to render the next data
        next={fetchData}
        hasMore={hasMore}
        loader={<Spinner />}
      > */}
      <div className="conference__container">
        {match.length > 0 &&
          match.map((el) => (
            <div key={el.id} className="conference__block">
              <div className="conference__bg">
                <div className="conference__bg-top">
                  {(new Date(el.regEnd).getDay() < new Date().getDay() &&
                    new Date(el.regEnd).getMonth() <= new Date().getMonth() &&
                    new Date(el.regEnd).getYear() === new Date().getYear() && (
                      <span
                        style={{
                          backgroundColor: "#939393",
                        }}
                      >
                        Регистрация закончена
                      </span>
                    )) ||
                    (new Date(el.dateEnd).getDay() < new Date().getDay() &&
                      new Date(el.dateEnd).getMonth() <=
                        new Date().getMonth() &&
                      new Date(el.dateEnd).getYear() ===
                        new Date().getYear() && (
                        <span
                          style={{
                            backgroundColor: "#939393",
                          }}
                        >
                          Конференция завершена
                        </span>
                      )) ||
                    (new Date().getDay() < new Date(el.regEnd).getDay() &&
                      new Date().getMonth() <= new Date(el.regEnd).getMonth() &&
                      new Date(el.regEnd).getYear() ===
                        new Date().getYear() && (
                        <span>Открыта регистрация</span>
                      ))}
                  <img
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
                  style={{ maxWidth: el.dateEnd.length ? "308px" : "200px" }}
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
                  {" "}
                  <div className="conference__title">{el.title}</div>
                </Link>
              </div>
            </div>
          ))}
        {match.length === 0 && (
          <div style={{ minHeight: "100vh" }}>
            <p>По запросу {value} ничего не найдено. </p>

            <p>Рекомендации:</p>

            <p>Убедитесь, что все слова написаны без ошибок.</p>
            <p>Попробуйте использовать другие ключевые слова.</p>
            <p>Попробуйте использовать более популярные ключевые слова.</p>
            <p>Попробуйте уменьшить количество слов в запросе.</p>
          </div>
        )}
      </div>
      {/* </InfiniteScroll> */}
    </section>
  );
};
export default SearchResult;
