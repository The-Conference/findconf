import React from "react";
import "../Login/login.scss";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { registerUser } from "../../store/userSlice";
import { useDispatch, useSelector } from "react-redux";
import CheckMail from "./CheckMail";
import close from "../../assets/close.svg";
const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordsMatch, setPasswordsMatch] = useState(false);

  const { user } = useSelector((state) => state);

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const handleNavigate = () => {
    navigate("/");
  };

  function handlePasswordChange(event) {
    setPassword(event.target.value);
    setPasswordsMatch(event.target.value === confirmPassword);
  }

  function handleConfirmPasswordChange(event) {
    setConfirmPassword(event.target.value);
    setPasswordsMatch(event.target.value === password);
  }

  const handleSignUp = (event) => {
    event.preventDefault();
    if (passwordsMatch) {
      dispatch(registerUser({ email, password }));
      setEmail("");
      setPassword("");
      setMessage("");
      setConfirmPassword("");
    }
  };
  useEffect(() => {
    if (user.error && user.error.email) {
      if (user.error.email.includes("Enter a valid email address.")) {
        setMessage("Пожалуйста введите правильный адрес почты");
      }
      if (user.error.email.includes("user with this email already exists.")) {
        setMessage("Пользователь с таким email уже существует");
      }
    }
    if (user.error && user.error.password) {
      if (
        user.error.password.includes(
          "This password is too short. It must contain at least 8 characters."
        ) ||
        user.error.password.includes("This password is too common.") ||
        user.error.password.includes("This password is entirely numeric.")
      ) {
        setMessage(
          "Пароль должен содержать не менее 8 символов и включать цифры и буквы"
        );
      }
    }
  }, [user.error]);
  return (
    <>
      {(user.registered === true && <CheckMail />) || (
        <div className="login">
          <img
            src={close}
            className="login__close"
            alt="close"
            onClick={handleNavigate}
          />
          <div className="login__welcome">
            <p className="login__welcome-black">Добро пожаловать</p>
            <p className="login__welcome-blue">в The Conference</p>{" "}
            <p className="login__welcome-grey">
              Конференции уже ждут твоего участия
            </p>
          </div>
          <form className="login__form" onSubmit={handleSignUp}>
            {/* <label htmlFor="">email</label> */}
            <div className="mail">
              <input
                type="email"
                id="email"
                autocomplete="new-email"
                className={message.length > 0 ? "red-border" : null}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <label
                htmlFor="email"
                className={email ? "filled-email " : "email "}
              >
                Email
              </label>
              {/* <label htmlFor="">пароль</label> */}
            </div>
            <div className="password">
              <input
                type="password"
                id="pass"
                autocomplete="new-password"
                value={password}
                className={message.length > 0 ? "red-border" : null}
                onChange={handlePasswordChange}
              />
              <label
                htmlFor="pass"
                className={password ? "filled-password " : "password "}
              >
                Пароль
              </label>
            </div>
            <div className="confirm-password">
              <input
                type="password"
                value={confirmPassword}
                className={message.length > 0 ? "red-border" : null}
                onChange={handleConfirmPasswordChange}
              />
              <label
                className={
                  confirmPassword
                    ? "filled-confirm-password"
                    : "confirm-password "
                }
              >
                Подтвердите пароль
              </label>
            </div>
            <button>Зарегистрироваться</button>
            <p className={passwordsMatch ? "match" : "error-message"}>
              {passwordsMatch && confirmPassword.length > 0
                ? "Пароли совпадают"
                : confirmPassword.length > 0 && !passwordsMatch
                ? "Пароли не совпадают"
                : null}
            </p>
            <div className="error-message">{message}</div>
          </form>
          <button className="login__button-grey">Восстановить пароль</button>
          <div className="login__hr">
            <hr />
            <span>или</span> <hr />
          </div>
          <a href="/login">
            <button className="login__button-blue">Войти</button>
          </a>
        </div>
      )}
    </>
  );
};

export default SignUp;
