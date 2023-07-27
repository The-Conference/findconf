import React from "react";
import notfound from "../../assets/404.svg";
import "./404.scss";
import "../UI kit/Buttons.scss";
const NotFound = () => {
  return (
    <div className="notfound">
      <div className="notfound-container">
        <div className="notfound-img">
          <img src={notfound} alt="не найдено" width="579" height="379" />
        </div>
        <div className="notfound-text">
          <h1>Что-то пошло не так(</h1>
          <p>Не волнуйся, мы уже работаем над ошибкой)</p>
          <a href="/">
            <button className="button button-large">Вернуться домой</button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
