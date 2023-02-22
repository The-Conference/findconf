import React, { useState, useEffect } from "react";
import hearts from "./follow.svg";
import following from "./following.svg";
import InfiniteScroll from "react-infinite-scroll-component";
import "./conference.scss";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import LoaderTemplate from "../../../utils/Loader/LoaderTemplate";
import { handleSave, handleFollow } from "../../../store/postData";

const AllConferences = () => {
  const dispatch = useDispatch();
  const { conferences } = useSelector((state) => state.conferences);
  // const LIMIT = 4;
  // const [postData, setPostData] = useState(conferences.slice(0, LIMIT));
  // const [visible, setVisible] = useState(LIMIT);
  // const [hasMore, setHasMore] = useState(true);
  const Favourite = JSON.parse(window.localStorage.getItem("fave")) || [];
  const [fave, setFave] = useState(Favourite);

  // const fetchData = () => {
  //   const newLimit = visible + LIMIT;
  //   const dataToAdd = conferences.slice(visible, newLimit);

  //   if (conferences.length > postData.length) {
  //     setTimeout(() => {
  //       setPostData([...postData].concat(dataToAdd));
  //     }, 1000);
  //     setVisible(newLimit);
  //   } else {
  //     setHasMore(false);
  //   }
  // };

  const handleFave = (id) => {
    if (fave.includes(id)) {
      setFave(fave.filter((el) => el !== id));
      console.log(fave);
    } else {
      setFave([...fave, id]);
    }
  };

  var options = { year: "numeric", month: "long", day: "numeric" };

  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);

  return (
    <section className="conference">
      <a href="/all">
        <p className="conference__type">
          Все конференции <span>&gt;</span>
        </p>
      </a>
      {/* <InfiniteScroll
        dataLength={postData.length}
        next={fetchData}
        hasMore={hasMore}
        loader={<LoaderTemplate />}
      > */}
      <div className="conference__container">
        {conferences.map((el) => (
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
        {conferences.length === 0 && <LoaderTemplate />}
      </div>
      {/* </InfiniteScroll> */}
    </section>
  );
};
console.log(AllConferences.data);
export default AllConferences;
