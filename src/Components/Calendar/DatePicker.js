/* eslint-disable react-hooks/exhaustive-deps */
import { addDays } from "date-fns";
import React, { useState } from "react";

import styles from "./DatePicker.module.css";
import { DateView } from "./DateView";
import { MonthView } from "./MonthView";
import CalendarFilter from "./CalendarFilter";
import calendar from "../../assets/calendar.svg";
import white from "../../assets/calwhite.svg";

const DatePicker = (props) => {
  const [showCalendar, setShowCalendar] = useState(false);

  const next = (event) => {
    event.preventDefault();
    const e = document.getElementById("container");
    const width = e ? e.getBoundingClientRect().width : null;
    e.scrollLeft += width - 60;
  };

  const startDate = props.startDate || new Date();
  const lastDate = addDays(startDate, props.days || 100);

  let Component = DateView;

  if (props.type === "month") {
    Component = MonthView;
  }
  const prev = (event) => {
    event.preventDefault();
    const e = document.getElementById("container");
    const width = e ? e.getBoundingClientRect().width : null;
    e.scrollLeft -= width - 60;
  };

  return (
    <div className={styles.container}>
      <div className={styles.buttonWrapper + " " + styles.buttonzIndex}>
        <span
          role="button"
          className={styles.calendar}
          style={{ backgroundColor: showCalendar ? "#184CD3" : "#ebefff" }}
          onClick={() => setShowCalendar(!showCalendar)}
        >
          {(!showCalendar && (
            <img src={calendar} alt="calendar" width="26" height="26" />
          )) || <img src={white} alt="calendar" width="26" height="26" />}
        </span>
        {showCalendar && (
          <CalendarFilter
            setShowCalendar={setShowCalendar}
            showCalendar={showCalendar}
          />
        )}
        <button className={styles.button} onClick={prev}>
          &lt;
        </button>
      </div>
      <Component {...props} startDate={startDate} lastDate={lastDate} />
      <div className={styles.buttonWrapper}>
        <button className={styles.button} onClick={next}>
          &gt;
        </button>
      </div>
    </div>
  );
};

export default DatePicker;
