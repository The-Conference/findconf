import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Filters from "../Components/Filters/Filters";
import { handleFollow, fetchAllConferences } from "../store/postData";
import { useSelector, useDispatch } from "react-redux";
import following from "./following.svg";
import hearts from "./follow.svg";
import { handleSave } from "../store/postData";
const SearchDate = () => {
  const { date } = useParams();
  const dispatch = useDispatch();
  const { conferences } = useSelector((state) => state.conferences);
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);
  var options = { year: "numeric", month: "long", day: "numeric" };
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
    const d1 = new Date(el.dateStart);
    const d2 = new Date(el.dateEnd);
    const id = el.id;
    let period = getDatesInRange(d1, d2);
    return { per: period, ind: id };
  });
  let amount = period.filter((el) => el.per.includes(date));
  let confs = amount.map((el) => el.ind);
  let match = conferences.filter((el) => confs.includes(el.id));

  useEffect(() => {
    dispatch(fetchAllConferences());
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
      <div className="conference__container">
        {conferences.length > 0 &&
          conferences
            .filter((el) => confs.includes(el.id))
            .map((el) => (
              <div key={el.id} className="conference__block">
                <div className="conference__bg">
                  <div className="conference__bg-top">
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
                    {el.tags.map((tag, index) => (
                      <small key={index}>{tag}</small>
                    ))}
                  </div>
                  <Link to={`/conferences/${el.id}`}>
                    <div className="conference__title">{el.title}</div>
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
