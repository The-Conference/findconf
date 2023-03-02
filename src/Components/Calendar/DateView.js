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
  // isSameDay,
  lastDayOfMonth,
  startOfMonth,
} from "date-fns";
import { Link } from "react-router-dom";

const DateView = ({
  startDate,
  lastDate,
  // selectDate,
  // getSelectedDay,
  primaryColor,
  labelFormat,
  marked,
}) => {
  // const [selectedDate, setSelectedDate] = useState(null);
  const { conferences } = useSelector((state) => state.conferences);

  const firstSection = { marginLeft: "40px" };
  // const selectedStyle = {
  //   fontWeight: "bold",
  //   width: "45px",
  //   height: "45px",
  //   borderRadius: "50%",
  //   border: `2px solid ${primaryColor}`,
  //   color: primaryColor,
  // };
  const labelColor = { color: primaryColor };
  // const markedStyle = { color: "#8c3737", padding: "2px", fontSize: 12 };

  // const getStyles = (day) => {
  //   return isSameDay(day, selectedDate) ? selectedStyle : null;
  // };

  // const getId = (day) => {
  //   return isSameDay(day, selectedDate) ? "selected" : "";
  // };

  // const getMarked = (day) => {
  //   let markedRes = marked?.find((i) => isSameDay(i.date, day));
  //   if (markedRes) {
  //     if (!markedRes?.marked) {
  //       return;
  //     }

  //     return (
  //       <div
  //         style={{ ...(markedRes?.style ?? markedStyle) }}
  //         className={styles.markedLabel}
  //       >
  //         {markedRes.text}
  //       </div>
  //     );
  //   }

  //   return "";
  // };
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

    // const styleItemMarked = marked ? styles.dateDayItemMarked : styles.dateDayItem;

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
            href={`/conferences/dates/${currentDay.toLocaleDateString()}`}
          >
            <div
              // id={`${getId(currentDay)}`}

              className={marked ? styles.dateDayItemMarked : styles.dateDayItem}
              key={currentDay}
              // onClick={() => onDateClick(currentDay)}
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

    return (
      <div id={"container"} className={styles.dateListScrollable}>
        {months}
      </div>
    );
  };

  // const onDateClick = (day) => {
  //   setSelectedDate(day);
  //   if (getSelectedDay) {
  //     getSelectedDay(day);
  //   }
  // };

  // useEffect(() => {
  //   if (getSelectedDay) {
  //     if (selectDate) {
  //       getSelectedDay(selectDate);
  //     } else {
  //       getSelectedDay(startDate);
  //     }
  //   }
  // }, []);

  // useEffect(() => {
  //   if (selectDate) {
  //     if (!isSameDay(selectedDate, selectDate)) {
  //       setSelectedDate(selectDate);
  //       setTimeout(() => {
  //         let view = document.getElementById("selected");
  //         if (view) {
  //           view.scrollIntoView({
  //             behavior: "smooth",
  //             inline: "center",
  //             block: "nearest",
  //           });
  //         }
  //       }, 20);
  //     }
  //   }
  // }, [selectDate]);

  return <React.Fragment>{renderDays()}</React.Fragment>;
};

export { DateView };
