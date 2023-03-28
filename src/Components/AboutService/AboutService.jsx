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
            <p>Январь 2023</p>
            <br />
            <ul>
              <li>Формирование ТЗ</li>
              <li>UX исследование</li>
              <li>Исследование на возможность парсинга данных</li>
            </ul>
          </div>
        </div>
        <div>
          <img src={step} alt="" />
          <div className="about__timeline-card">
            <p>Февраль 2023</p>
            <br />
            <ul>
              <li>Верстка страниц, календаря, фильтров</li>
              <li>Формирование БД</li>
              <li> Отрисовка иллюстраций</li>
              <li> Интеграция фронта с беком</li>
            </ul>
          </div>
        </div>
        <div>
          <img src={step} alt="" />
          <div className="about__timeline-card last">
            <p>Март 2023</p>
            <br />
            <ul>
              <li>Регистрация домена</li>
              <li>Тестирование</li>
              <li>Верстка адаптива</li>
              <li>Работа с багами</li>
              <li>Запуск прод версии</li>
            </ul>
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
              <div className="name">
                <a
                  href={`https://t.me/${el.tg}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  <p>{el.name}</p>
                </a>
                <svg
                  width="6"
                  height="10"
                  viewBox="0 0 6 10"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M0.999779 9.75002C0.807779 9.75002 0.61575 9.67705 0.46975 9.53005C0.17675 9.23705 0.17675 8.76202 0.46975 8.46902L3.93972 4.99905L0.46975 1.52908C0.17675 1.23608 0.17675 0.761041 0.46975 0.468041C0.76275 0.175041 1.23779 0.175041 1.53079 0.468041L5.53079 4.46804C5.82379 4.76104 5.82379 5.23608 5.53079 5.52908L1.53079 9.52908C1.38379 9.67708 1.19178 9.75002 0.999779 9.75002Z"
                    fill="#00002E"
                  />
                </svg>
              </div>
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
              <div className="name">
                <a
                  href={`https://t.me/${el.tg}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  <p>{el.name}</p>
                </a>
                <svg
                  width="6"
                  height="10"
                  viewBox="0 0 6 10"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M0.999779 9.75002C0.807779 9.75002 0.61575 9.67705 0.46975 9.53005C0.17675 9.23705 0.17675 8.76202 0.46975 8.46902L3.93972 4.99905L0.46975 1.52908C0.17675 1.23608 0.17675 0.761041 0.46975 0.468041C0.76275 0.175041 1.23779 0.175041 1.53079 0.468041L5.53079 4.46804C5.82379 4.76104 5.82379 5.23608 5.53079 5.52908L1.53079 9.52908C1.38379 9.67708 1.19178 9.75002 0.999779 9.75002Z"
                    fill="#00002E"
                  />
                </svg>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
export default AboutService;
