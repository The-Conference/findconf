import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import "./fullconference.scss";
const FullConference = () => {
  const { conferences } = useSelector((state) => state.conferences);
  const { itemId } = useParams();
  let conf = 0;
  let full = conferences.find(({ id }) => id === itemId);
  if (full) {
    conf = full;
  }
  console.log(conferences);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="full-conference">
      {(conf === 0 && <div style={{ height: "100vh" }}>404</div>) || (
        <div className="full-conference__container">
          <h1>{conf.title}</h1>
          <div>Основная информация</div>
          <div>
            {" "}
            <span>описание:</span>
            {conf.description}
          </div>
          <div>
            <span>адрес проведения:</span>
            {conf.address}
          </div>
          <div>
            <span>ссылка на конференцию:</span>
            {conf.link}
          </div>
          <div>
            <span>начало регистрации</span>
            {conf.regStart}
          </div>
          <div>
            <span>окончание регистрации:</span>
            {conf.regEnd}
          </div>
          <div>
            <span>контакты:</span>
            {conf.contacts}
          </div>
          <div>
            <span>организатор:</span>
            {conf.organizer}
          </div>
          <div>
            <span>дата проведения:</span>
            {conf.dateStart}-{conf.dateEnd}
          </div>
          {(conf.online === true && (
            <div>
              {" "}
              <span>форма:</span>онлайн
            </div>
          )) ||
            (conf.offline === true && (
              <div>
                {" "}
                <span>форма:</span>онлайн
              </div>
            )) || (
              <div>
                {" "}
                <span>форма:</span>уточняется
              </div>
            )}
        </div>
      )}
    </div>
  );
};
export default FullConference;
