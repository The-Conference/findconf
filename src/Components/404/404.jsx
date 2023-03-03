import React from "react";
import notfound from "../../assets/404.svg";
import "./404.scss";
const NotFound = () => {
  return (
    <div className="notfound">
      <div className="notfound-container">
        <img src={notfound} alt="не найдено" />
        <div>
          <h1>Что-то пошло не так(</h1>
          <p>Не волнуйся, мы уже работаем над ошибкой)</p>
          <a href="/">
            <button>Вернуться домой</button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
