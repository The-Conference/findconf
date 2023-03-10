export const getDatesInRange = (startDate, endDate) => {
  const date = new Date(startDate.getTime());
  date.setDate(date.getDate() + 1);
  const dates = [startDate, endDate];
  while (date < endDate) {
    dates.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return dates.map((el) => el.toLocaleDateString());
};
