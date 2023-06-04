import React from "react";
import "../Login/login.scss";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { registerUser } from "../../store/userSlice";
import { useDispatch, useSelector } from "react-redux";
import Registered from "../SignUp/Registered";

const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const { user } = useSelector((state) => state);
  console.log(user.registered);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const handleNavigate = () => {
    navigate("/");
  };
  const handleSignUp = (event) => {
    event.preventDefault();
    dispatch(registerUser({ email, password }));
    setEmail("");
    setPassword("");
  };

  return (
    <>
      {(user.registered === false && (
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
          <form className="login__form" action="" onSubmit={handleSignUp}>
            {/* <label htmlFor="">email</label> */}
            <input
              type="mail"
              value={email}
              placeholder="E-mail"
              onChange={(e) => setEmail(e.target.value)}
            />
            {/* <label htmlFor="">пароль</label> */}
            <input
              type="password"
              value={password}
              placeholder="Пароль"
              onChange={(e) => setPassword(e.target.value)}
            />
            {/* <label htmlFor=""></label>{" "}
        <input type="password" placeholder="Подтвердить пароль" />
        <div className="login__form-agreement">
          <input type="checkbox" />
          <label htmlFor="">
            Я принимаю условия
            <span>Пользовательского соглашения</span>
          </label>
        </div> */}
            <button>Зарегистрироваться</button>
          </form>
          <button className="login__button-grey">Восстановить пароль</button>
          <div className="login__hr">
            <hr />
            <span>или</span> <hr />
          </div>
          <a href="/login">
            <button className="login__button-blue">Войти</button>
          </a>
          <div>{message}</div>
        </div>
      )) || <Registered />}
    </>
  );
};

export default SignUp;
