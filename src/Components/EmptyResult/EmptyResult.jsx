import React from "react";
import empty from "../../assets/emptyresult.svg";
import "./empty-result.scss";
const EmptyResult = () => {
  return (
    <div className="empty">
      <img src={empty} alt="пусто" width="450" height="350" />
      <h3>Эхх...</h3>
      <p>
        По данному запросу конференций нет, попробуй использовать другие фильтры
        или ключевые слова :){" "}
      </p>
    </div>
  );
};

export default EmptyResult;
