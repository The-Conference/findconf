import React from "react";
import step from "../../assets/Step.svg";
import "./about.scss";
import { developers, founders } from "../../utils/Founders/FOUNDERS";

const AboutService = () => {
  return (
    <div className="about">
      <h1>
        Немного о <span>нашем</span> сервисе
      </h1>

      <p className="about__launched">
        Сервис был запущен в 2023 году с целью упрощения поиска конференций для
        студентов различных направлений и профессионалов своего дела
      </p>

      <div className="about__timeline">
        <div>
          <img src={step} alt="" />
          <div className="about__timeline-card">
            <p>15.12.2022</p>
            <br />
            <p>
              Создание концепции, формирование командыСоздание концепции,
              формирование командыСоздание концепции, формирование
              командыформирование{" "}
            </p>
          </div>
        </div>
        <div>
          <img src={step} alt="" />
          <div className="about__timeline-card">
            <p>15.12.2022</p>
            <br />
            <p>
              Создание концепции, формирование командыСоздание концепции,
              формирование командыСоздание концепции, формирование
              командыформирование{" "}
            </p>
          </div>
        </div>
        <div>
          <img src={step} alt="" />
          <div className="about__timeline-card last">
            <p>15.12.2022</p>
            <br />
            <p>
              Создание концепции, формирование командыСоздание концепции,
              формирование командыСоздание концепции, формирование
              командыформирование{" "}
            </p>
          </div>
        </div>
      </div>
      <div className="about__staff">
        <h1>
          Создатели <span>The Conference</span>
        </h1>
        <h2>Руководство</h2>

        <div className="about__staff-container">
          {founders.map((el, index) => (
            <div key={index} className="about__staff-founders">
              <div className="about__staff-founders-pic">
                <img src={el.pic} alt="фото" width={300} height={300} />
              </div>
              <div className="role">{el.role}</div>

              <p>{el.name}</p>
            </div>
          ))}
        </div>
        <h2>Разработчики</h2>
        <div className="about__staff-container">
          {developers.map((el, index) => (
            <div key={index} className="about__staff-founders">
              <div className="about__staff-founders-pic">
                <img src={el.pic} alt="фото" width={300} height={300} />
              </div>
              <div className="role">{el.role}</div>
              <p>{el.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
export default AboutService;
