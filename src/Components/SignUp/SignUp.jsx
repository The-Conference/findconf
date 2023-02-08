import React from "react";
import "../Login/login.scss";
const SignUp = () => {
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
        <input type="password" placeholder="Подтвердить пароль" />

        <div className="login__form-agreement">
          <input type="checkbox" />
          <label htmlFor="">
            Я принимаю условия
            <span>Пользовательского соглашения</span>
          </label>
        </div>
        <button>Зарегистрироваться</button>
      </form>
      <button className="login__button-grey">Восстановить пароль</button>
      <div className="login__hr">
        <hr />
        <span>или</span> <hr />
      </div>
      <button className="login__button-blue">Войти</button>
    </div>
  );
};

export default SignUp;
