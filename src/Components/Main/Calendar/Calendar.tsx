import React from "react";
import {
  Datepicker,
  DatepickerEvent,
} from "@meinefinsternis/react-horizontal-date-picker";
import { ru } from "date-fns/locale";
import "./calendar.scss";
import calendar from "./calendar.svg";
const Calendar = () => {
  const [date, setDate] = React.useState<{
    endValue: Date | null;
    startValue: Date | null;
    rangeDates: Date[] | null;
  }>({
    startValue: null,
    endValue: null,
    rangeDates: [],
  });

  const handleChange = (d: DatepickerEvent) => {
    const [startValue, endValue, rangeDates] = d;
    setDate((prev) => ({ ...prev, endValue, startValue, rangeDates }));
    console.log(date);
  };
  return (
    <div className="datepicker">
      <span>
        <img src={calendar} alt="datepicker" />
      </span>
      <Datepicker
        onChange={handleChange}
        locale={ru}
        startValue={date.startValue}
        endValue={date.endValue}
      />
    </div>
  );
};

export default Calendar;
