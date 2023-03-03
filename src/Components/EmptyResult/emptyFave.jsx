import React from "react";
import empty from "../../assets/emptyresult.svg";
import "./empty-result.scss";
const EmptyFave = () => {
  return (
    <div className="empty">
      <img src={empty} alt="пусто" />
      <p>Не найдено ни одной конференции</p>
    </div>
  );
};

export default EmptyFave;
