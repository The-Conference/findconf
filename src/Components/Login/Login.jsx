import { useState, useEffect } from "react";
import "./login.scss";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login } from "../../store/authSlice";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import close from "../../assets/close.svg";

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
    setTimeout(() => {
      setEmail("");
      setPassword("");
      setMessage("");
      if (!isAuthenticated) {
        setMessage("Неверный пароль или логин");
      }
    }, 2000);
  };
  useEffect(() => {
    if (isAuthenticated) {
      nav("/");
    }
  }, [isAuthenticated, nav]);

  return (
    <div className="login">
      <Link to="/" className="login__close">
        <img src={close} alt="close" />
      </Link>
      <div className="login__welcome">
        <p className="login__welcome-black">Добро пожаловать</p>
        <p className="login__welcome-blue">в The Conference</p>{" "}
        <p className="login__welcome-grey">
          Конференции уже ждут твоего участия
        </p>
      </div>
      <form
        autocomplete="new-password"
        className="login__form"
        action=""
        onSubmit={handleSubmit}
      >
        <div className="mail">
          <input
            type="mail"
            autocomplete="new-password"
            className={message.length > 0 ? "red-border" : null}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <label className={email ? "filled-email " : "email "}>Email</label>
        </div>
        <div className="password">
          <input
            type="password"
            autocomplete="new-password"
            className={message.length > 0 ? "red-border" : null}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label className={password ? "filled-password " : "password "}>
            Password
          </label>
        </div>
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
