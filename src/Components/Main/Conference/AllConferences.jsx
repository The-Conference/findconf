import React from "react";
import hearts from "./follow.svg";
import following from "./following.svg";
// import Spinner from "../../../utils/Loader/Spinner";
// import InfiniteScroll from "react-infinite-scroll-component";
import Filters from "../../Filters/Filters";
import { handleFollow, card } from "../../../store/postData";
import { useDispatch, useSelector } from "react-redux";

const AllConferences = (
  {
    // fetchData,
    // hasMore,
  }
) => {
  const dispatch = useDispatch();
  const data = useSelector(card);

  return (
    <section className="conference">
      <a href="/">
        <p className="conference__type">
          Все конференции <span>&gt;</span>
        </p>
      </a>
      <Filters />
      {/* <InfiniteScroll
        dataLength={postData.length} //This is important field to render the next data
        next={fetchData}
        hasMore={hasMore}
        loader={<Spinner />}
      > */}
      <div className="conference__container">
        {data.length > 0 &&
          data.map((el) => (
            <div el={el.id} className="conference__block">
              <div className="conference__bg">
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
              <div className="conference__tags">
                {el.tags.map((tag) => (
                  <small>{tag}</small>
                ))}

                <div className="conference__title">{el.title}</div>
                <div className="conference__organizer">
                  <p>Организатор:</p>
                  {el.organizer}
                </div>
                <div className="conference__date">
                  <p>Дата проведения:</p>
                  {el.date}
                </div>
              </div>
            </div>
          ))}
        {data.length === 0 && <div>нет такой конфы беач</div>}
      </div>
      {/* </InfiniteScroll> */}
    </section>
  );
};
export default AllConferences;
