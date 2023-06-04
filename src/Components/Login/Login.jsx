import { useState, useEffect } from "react";
import "./login.scss";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login } from "../../store/authSlice";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const nav = useNavigate();

  const isAuthenticated = useSelector((state) => state.auth.token !== null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    dispatch(login({ email, password }));
    setEmail("");
    setPassword("");
    setMessage("");
    if (!isAuthenticated) {
      setMessage("Неверный пароль или логин");
    }
  };
  useEffect(() => {
    if (isAuthenticated) {
      nav("/profile");
    }
  }, [isAuthenticated, nav]);

  return (
    <div className="login">
      <Link to="/" className="login__close">
        x
      </Link>
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
          className={message.length > 0 ? "red-border" : null}
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          className={message.length > 0 ? "red-border" : null}
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button>Войти</button>
        <div className="error-message">{message}</div>
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
