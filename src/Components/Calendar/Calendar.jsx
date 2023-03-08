import React from "react";
import DatePicker from "./DatePicker";

function Calendar() {
  const startDate = new Date();

  return (
    <div>
      <DatePicker
        startDate={startDate}
        type="day"
        selectDate={new Date()}
        labelFormat={"LLLL"}
        color={"none"}
      />
    </div>
  );
}

export default Calendar;
