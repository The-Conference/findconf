import React from "react";
import {
  Datepicker,
  DatepickerEvent,
} from "@meinefinsternis/react-horizontal-date-picker";
import { ru } from "date-fns/locale";
import "./calendar.scss";
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
    console.log(date.startValue);
  };

  return (
    <Datepicker
      onChange={handleChange}
      locale={ru}
      startValue={date.startValue}
      endValue={date.endValue}
    />
  );
};

export default Calendar;
