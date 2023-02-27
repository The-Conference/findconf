import React, { useState, useEffect } from "react";
import hearts from "./follow.svg";
import following from "./following.svg";
// import InfiniteScroll from "react-infinite-scroll-component";
import "./conference.scss";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import LoaderTemplate from "../../../utils/Loader/LoaderTemplate";
import { handleSave, handleFollow, card } from "../../../store/postData";
import Filters from "../../Filters/Filters";
const AllConferences = () => {
  const dispatch = useDispatch();
  const { conferences, isLoading } = useSelector((state) => state.conferences);
  const data = useSelector(card);
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
  useEffect(() => {
    dispatch(handleSave(fave));
  }, [fave]);
  console.log(conferences);
  return (
    <section className="conference">
      <p className="conference__type">
        Все конференции <span>&gt;</span>
      </p>
      <Filters />
      {/* <InfiniteScroll
        dataLength={postData.length}
        next={fetchData}
        hasMore={hasMore}
        loader={<LoaderTemplate />}
      > */}
      {/* <Filters /> */}
      <div className="conference__container">
        {(!isLoading && <LoaderTemplate />) ||
          (isLoading &&
            conferences.map((el) => (
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
            )))}
      </div>{" "}
      {/* </InfiniteScroll> */}
    </section>
  );
};

export default AllConferences;

// const LIMIT = 4;
// const [postData, setPostData] = useState(conferences.slice(0, LIMIT));
// const [visible, setVisible] = useState(LIMIT);
// const [hasMore, setHasMore] = useState(true);

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
