import React from "react";
import DatePicker from "./DatePicker";

function Calendar({ card }) {
  const startDate = new Date();

  return (
    <div>
      <DatePicker
        card={card}
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
