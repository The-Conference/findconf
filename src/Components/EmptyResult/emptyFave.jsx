import React from "react";
import empty from "../../assets/emptyresult.svg";
import "./empty-result.scss";
const EmptyFave = () => {
  return (
    <div className="empty">
      <img src={empty} alt="пусто" />
      <p>Добавьте интересные конференции в избранное </p>
    </div>
  );
};

export default EmptyFave;
