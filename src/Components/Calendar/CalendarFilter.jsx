import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./calendarFilter.css";
import { useNavigate } from "react-router-dom";

const CalendarFilter = () => {
  const nav = useNavigate();
  const [value, onChange] = useState(new Date());

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
    <div className="calender-filter">
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
