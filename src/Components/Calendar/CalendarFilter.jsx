import React, { useState, useRef } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./calendarFilter.css";
import { useNavigate } from "react-router-dom";
import useOnClickOutside from "../Hooks/useOnClickOutside";
import cross from "../../assets/Cross.svg";
const CalendarFilter = ({ setShowCalendar }) => {
  const nav = useNavigate();
  const ref = useRef();
  const [value, onChange] = useState(new Date());
  useOnClickOutside(ref, () => setShowCalendar(false));
  const handleDates = (value) => {
    nav(
      `/dates/${
        typeof value === "string"
          ? value.toLocaleDateString()
          : value.map((el) => el.toISOString()).join(",")
      }`
    );
  };

  return (
    <div className="calender-filter" ref={ref}>
      <span className="close-calendar" onClick={() => setShowCalendar(false)}>
        <img src={cross} alt="закрыть" />
      </span>
      <Calendar
        selectRange={true}
        onChange={onChange}
        allowPartialRange={false}
      />
      <button onClick={() => handleDates(value)} className="find">
        Найти
      </button>
    </div>
  );
};
export default CalendarFilter;
