/* eslint-disable react-hooks/exhaustive-deps */
import React from "react";
import styles from "./DatePicker.module.css";
import { ru } from "date-fns/locale";
import { useSelector } from "react-redux";

import {
  addDays,
  addMonths,
  differenceInMonths,
  format,
  lastDayOfMonth,
  startOfMonth,
} from "date-fns";

const DateView = ({
  startDate,
  lastDate,
  primaryColor,
  labelFormat,
  marked,
  count,
  setCount,
}) => {
  const { conferences } = useSelector((state) => state.conferences);
  const firstSection = { marginLeft: "40px" };
  const labelColor = { color: primaryColor };

  function getDatesInRange(startDate, endDate, id) {
    const date = new Date(startDate.getTime());

    date.setDate(date.getDate() + 1);

    const dates = [startDate, endDate];

    while (date < endDate) {
      dates.push(new Date(date));
      date.setDate(date.getDate() + 1);
    }

    return dates.map((el) => el.toLocaleDateString());
  }
  let period = conferences.map((el) => {
    const d1 = new Date(el.conf_date_begin);
    const d2 = new Date(el.conf_date_end);
    const id = el.id;

    let period = getDatesInRange(d1, d2);
    return { per: period, ind: id };
  });

  const renderDays = () => {
    const dayFormat = "EEEEEE";
    const dateFormat = "d";

    const months = [];
    let days = [];
    for (let i = 0; i <= differenceInMonths(lastDate, startDate); i++) {
      let start, end;
      const month = startOfMonth(addMonths(startDate, i));

      start = i === 0 ? Number(format(startDate, dateFormat)) - 1 : 0;
      end =
        i === differenceInMonths(lastDate, startDate)
          ? Number(format(lastDate, "d"))
          : Number(format(lastDayOfMonth(month), "d"));

      for (let j = start; j < end; j++) {
        let currentDay = addDays(month, j);

        days.push(
          <a
            key={j}
            style={{
              pointerEvents:
                period.filter((el) =>
                  el.per.includes(currentDay.toLocaleDateString())
                ).length === 0
                  ? "none"
                  : "auto",
              cursor:
                period.filter((el) =>
                  el.per.includes(currentDay.toLocaleDateString())
                ).length === 0
                  ? "not-allowed"
                  : "pointer",
            }}
            href={`/date/${currentDay.toLocaleDateString()}`}
          >
            <div
              className={marked ? styles.dateDayItemMarked : styles.dateDayItem}
              key={currentDay}
            >
              <div
                className={styles.dayLabel}
                style={{
                  color:
                    currentDay.getDay() === 6 || currentDay.getDay() === 0
                      ? "#D1413780"
                      : "#00002E4D",
                }}
              >
                {format(currentDay, dayFormat, { locale: ru })}
              </div>
              <div
                className={styles.dateLabel}
                style={{
                  color:
                    currentDay.getDay() === 6 || currentDay.getDay() === 0
                      ? "#D14137"
                      : "#00002E",
                }}
              >
                {format(currentDay, dateFormat, { locale: ru })}
              </div>

              <div
                className={styles.amount}
                style={{
                  color:
                    currentDay.getDay() === 6 || currentDay.getDay() === 0
                      ? "#D1413780"
                      : "#00003880",
                }}
              >
                {
                  period.filter((el) =>
                    el.per.includes(currentDay.toLocaleDateString())
                  ).length
                }
              </div>
            </div>
          </a>
        );
      }

      months.push(
        <div className={styles.monthContainer} key={month}>
          <span className={styles.monthYearLabel} style={labelColor}>
            {format(month, labelFormat || "MMMM yyyy", { locale: ru })}
          </span>
          <div
            className={styles.daysContainer}
            style={i === 0 ? firstSection : null}
          >
            {days}
          </div>
        </div>
      );
      days = [];
    }
    const handleScroll = () => {
      const e = document.getElementById("container");
      if (e.scrollLeft > 6) {
        setCount(1);
      } else {
        setCount(0);
      }
    };
    return (
      <div
        id={"container"}
        className={styles.dateListScrollable}
        onScroll={handleScroll}
      >
        {months}
      </div>
    );
  };
  return <React.Fragment>{renderDays()}</React.Fragment>;
};

export { DateView };
