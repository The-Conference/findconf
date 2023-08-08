import React, { useState } from "react";
import step from "../../assets/Step.svg";
import "./about.scss";
import { developers, founders } from "../../utils/Founders/FOUNDERS";

const AboutService = () => {
  const [isLoading, setIsLoading] = useState(true);

  const handleImageLoad = () => {
    setIsLoading(false);
  };

  const renderStaff = (staff) => {
    return staff.map((el) => (
      <div key={el.name} className="about__staff-founders">
        <div
          className={`'about__staff-founders-pic' ${
            isLoading
              ? " about__staff-founders-pic blur"
              : "about__staff-founders-pic"
          }`}
        >
          {isLoading && <div className="blur-image-placeholder"></div>}
          <img
            onLoad={handleImageLoad}
            src={el.pic}
            alt="фото"
            width={300}
            height={300}
            className={`'' ${isLoading ? "hidden" : ""}`}
          />
        </div>
        <div className="role">{el.role}</div>
        <div className="name">
          <p>{el.name}</p>
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
    ));
  };

  const renderTimelineItem = (date, items, last = false) => {
    return (
      <div>
        <img src={step} alt="" />
        <div className={`about__timeline-card${last ? " last" : ""}`}>
          <p>{date}</p>
          <br />
          <ul>
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    );
  };

  const renderTimeline = () => {
    return (
      <div className="about__timeline">
        {[
          {
            date: "Январь 2023",
            items: [
              "Формирование ТЗ",
              "UX исследование",
              "Исследование на возможность парсинга данных",
            ],
          },
          {
            date: "Февраль 2023",
            items: [
              "Верстка страниц, календаря, фильтров",
              "Формирование БД",
              "Отрисовка иллюстраций",
              "Интеграция фронта с беком",
            ],
          },
          {
            date: "Март 2023",
            items: [
              "Регистрация домена",
              "Тестирование",
              "Верстка адаптива",
              "Работа с багами",
              "Запуск прод версии",
            ],
            last: true,
          },
        ].map((timelineItem, index) =>
          renderTimelineItem(
            timelineItem.date,
            timelineItem.items,
            timelineItem.last
          )
        )}
      </div>
    );
  };

  return (
    <div className="about">
      <h1>
        Немного о <span>нашем</span> сервисе
      </h1>

      <p className="about__launched">
        Сервис был запущен в 2023 году с целью упрощения поиска конференций для
        студентов различных направлений и профессионалов своего дела
      </p>

      {renderTimeline()}

      <div className="about__staff">
        <h1>
          Создатели <span>The Conference</span>
        </h1>
        <h2>Руководство</h2>

        <div className="about__staff-container">{renderStaff(founders)}</div>

        <h2>Разработчики</h2>
        <div className="about__staff-container">{renderStaff(developers)}</div>
      </div>
    </div>
  );
};

export default AboutService;
