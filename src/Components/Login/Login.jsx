import React from "react";
import "./login.scss";
const Login = () => {
  return (
    <div className="login">
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
