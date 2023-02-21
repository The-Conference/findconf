import React from "react";
import hearts from "./follow.svg";
import following from "./following.svg";
// import InfiniteScroll from "react-infinite-scroll-component";
import "./conference.scss";
import { useSelector, useDispatch } from "react-redux";
import { handleFollow } from "../../../store/postData";
import { Link } from "react-router-dom";
import LoaderTemplate from "../../../utils/Loader/LoaderTemplate";
const AllConferences = ({ fetchData, hasMore }) => {
  const { conferences } = useSelector((state) => state.conferences);
  const dispatch = useDispatch();
  console.log(conferences);
  var options = { year: "numeric", month: "long", day: "numeric" };

  return (
    <section className="conference">
      <a href="/all">
        <p className="conference__type">
          Все конференции <span>&gt;</span>
        </p>
      </a>
      {/* <InfiniteScroll
        dataLength={postData.length} //This is important field to render the next data
        next={fetchData}
        hasMore={hasMore}
        loader={<Spinner />}
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
                  onClick={() => dispatch(handleFollow(el.id))}
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
