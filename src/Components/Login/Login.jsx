import React from "react";
import "./login.scss";
import { useNavigate } from "react-router-dom";
const Login = () => {
  const navigate = useNavigate();
  const handleNavigate = () => {
    navigate("/");
  };
  return (
    <div className="login">
      <span className="login__close" onClick={handleNavigate}>
        x
      </span>
      <div className="login__welcome">
        <p className="login__welcome-black">Добро пожаловать</p>
        <p className="login__welcome-blue">в The Conference</p>{" "}
        <p className="login__welcome-grey">
          Конференции уже ждут твоего участия
        </p>
      </div>
      <form className="login__form" action="">
        <input type="mail" placeholder="E-mail" />
        <input type="password" placeholder="Пароль" />
        <button>Войти</button>
      </form>
      <button className="login__button-grey">Восстановить пароль</button>
      <div className="login__hr">
        <hr />
        <span>или</span> <hr />
      </div>
      <a href="/signup">
        <button className="login__button-blue">Зарегистрироваться</button>
      </a>
    </div>
  );
};

export default Login;
