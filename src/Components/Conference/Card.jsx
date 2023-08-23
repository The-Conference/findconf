import React from "react";
import { DateFormatter } from "../../utils/options";
import FollowButton from "../FollowButton/FollowButton";
const Card = ({ el }) => {
  return (
    <div key={el.id} className="conference__block">
      <div className="conference__wrapper">
        <div className="conference__tags">
          <div className="conference__tags-name">
            {el.tags.map((elem) =>
              elem.name
                .split(",")
                .map((tag, index) => <span key={index}>{tag}</span>)
            )}
            {el.online === true && <span>Онлайн</span>}
            {el.offline === true && <span>Офлайн</span>}
            <span>{el.conf_status}</span>
          </div>
          <FollowButton id={el.id} favorite={el.is_favorite} type={"card"} />
        </div>
        <h2 className="conference__title">{el.conf_name}</h2>
        <p className="conference__text">
          Lorem ipsum dolor sit amet consectetur, adipisicing elit. Explicabo
          suscipit temporibus nihil illum nisi error accusantium, numquam eius
          nobis excepturi quod iste ex, dicta magnam omnis quis ea molestiae
          quas. Lorem ipsum dolor sit amet consectetur, adipisicing elit.
          Explicabo suscipit temporibus nihil illum nisi error accusantium,
          numquam eius nobis excepturi quod iste ex, dicta magnam omnis quis ea
          molestiae quas. Lorem ipsum dolor sit amet consectetur, adipisicing
          elit. Explicabo suscipit temporibus nihil illum nisi error
          accusantium, numquam eius nobis excepturi quod iste ex, dicta magnam
          omnis quis ea molestiae quas.
        </p>
        <a
          className="conference__more"
          aria-label="Подробнее о конференции"
          href={`/conferences/${el.id}`}
        >
          <span></span>
        </a>
        <a
          className="conference__more2"
          aria-label="Подробнее о конференции"
          href={`/conferences/${el.id}`}
        >
          <span></span>
        </a>
        <div className="conference__date">
          Дата проведения:
          <span>{DateFormatter(el)}</span>
        </div>
      </div>
    </div>
  );
};

export default Card;
