import React from "react";
import check from "../../assets/check-mail.svg";
import "./check-mail.scss";
const CheckMail = () => {
  return (
    <div className="check-mail">
      <div className="check-mail__container">
        <div className="check-mail__title">
          Проверь <span>почту</span>
        </div>
        <div className="check-mail__text">
          Мы отправили ссылку на указанную почту. Если письмо не пришло в
          течение 10 минут, то проверь папку «Спам»
        </div>
        <img className="check-mail__img" src={check} alt="check" />
        <button className="check-mail__button">
          <a href="/">Вернуться на главную</a>
        </button>
      </div>
    </div>
  );
};
export default CheckMail;
