export const options = { year: "numeric", month: "long", day: "numeric" };

export const DateFormatter = (data) => {
  return data.conf_date_end === null
    ? new Date(data.conf_date_begin)
        .toLocaleDateString("ru", options)
        .slice(0, -3)
    : data.conf_date_begin === null
    ? new Date(data.conf_date_end)
        .toLocaleDateString("ru", options)
        .slice(0, -3)
    : data.conf_date_end !== data.conf_date_begin
    ? new Date(data.conf_date_begin)
        .toLocaleDateString("ru", options)
        .slice(0, -3) +
      " - " +
      new Date(data.conf_date_end)
        .toLocaleDateString("ru", options)
        .slice(0, -3)
    : new Date(data.conf_date_begin)
        .toLocaleDateString("ru", options)
        .slice(0, -3);
};
