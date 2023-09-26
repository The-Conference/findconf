import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import "./registered.scss";
import welcome from "../../assets/welcome.svg";
import axios from "axios";
import { useParams } from "react-router-dom";

const Registered = () => {
  const { token, uid } = useParams();

  useEffect(() => {
    const confirmRegistration = async () => {
      try {
        const response = await axios.post(
          `https://theconf.ru/api/auth/users/activation/`,
          { uid, token }
        );
        console.log(response);
      } catch (error) {
        console.log(error);
      }
    };

    confirmRegistration();
  }, [token, uid]);

  return (
    <div className="registered">
      <div className="registered__container">
        <div className="registered__title">
          Ты часть <br /> <span>The Conference!</span>{" "}
        </div>

        <img className="registered__img" src={welcome} alt="welcome" />
        <Link className="registered__link" to="/login">
          <div className="registered__button"> Авторизоваться</div>
        </Link>
      </div>
    </div>
  );
};
export default Registered;
