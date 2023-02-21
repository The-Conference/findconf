import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./calendarFilter.css";

const CalendarFilter = () => {
  const [value, onChange] = useState(new Date());

  return (
    <div className="calender-filter">
      <Calendar onChange={onChange} value={value} />
    </div>
  );
};
export default CalendarFilter;
