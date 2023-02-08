import React from "react";
import heart from "./follow.svg";
import following from "./following.svg";
import { useState } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import LoaderTemplate from "../../../utils/Loader/LoaderTemplate";

const LIMIT = 8;

const AllConferences = ({ card, setCard, handleFollow }) => {
  const [postData, setPostData] = useState(card.slice(0, LIMIT));
  const [visible, setVisible] = useState(LIMIT);
  const [hasMore, setHasMore] = useState(true);

  const fetchData = () => {
    const newLimit = visible + LIMIT;
    const dataToAdd = card.slice(visible, newLimit);

    if (card.length > postData.length) {
      setTimeout(() => {
        setPostData([...postData].concat(dataToAdd));
      }, 1000);
      setVisible(newLimit);
    } else {
      setHasMore(false);
    }
  };

  return (
    <section className="conference">
      <a href="/">
        <p className="conference__type">
          Все конференции <span>&gt;</span>
        </p>
      </a>
      <InfiniteScroll
        dataLength={postData.length} //This is important field to render the next data
        next={fetchData}
        hasMore={hasMore}
        loader={<LoaderTemplate />}
      >
        <div className="conference__container">
          {postData.map((el) => (
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
                  src={el.follow === false ? heart : following}
                  alt="follow"
                  onClick={() => handleFollow(el.id)}
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
          ))}{" "}
        </div>
      </InfiniteScroll>
    </section>
  );
};
export default AllConferences;
