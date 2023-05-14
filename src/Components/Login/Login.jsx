import { useState } from "react";
import "./login.scss";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login } from "../../store/authSlice";

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    dispatch(login({ email, password }));
    setEmail("");
    setPassword("");
    navigate("/profile");
  };

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
      <form className="login__form" action="" onSubmit={handleSubmit}>
        <input
          type="mail"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
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
