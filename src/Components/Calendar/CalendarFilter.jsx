import React, { useState, useRef, useEffect } from "react";
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
    value.length === 1
      ? nav(`/date/${value.map((el) => el.toLocaleDateString())}`)
      : nav(`/dates/${value.map((el) => el.toISOString()).join(",")}`);
  };
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);
  return (
    <div className="calender-filter" ref={ref}>
      <span className="close-calendar" onClick={() => setShowCalendar(false)}>
        <img src={cross} alt="закрыть" />
      </span>
      <Calendar
        selectRange={true}
        onChange={onChange}
        allowPartialRange={true}
      />
      <button onClick={() => handleDates(value)} className="find">
        Найти
      </button>
    </div>
  );
};
export default CalendarFilter;
