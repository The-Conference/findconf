export const dateToYMD = (date) => {
  var d = date.getDate();
  var m = date.getMonth() + 1;
  return "" + (m <= 9 ? "0" + m : m) + "-" + (d <= 9 ? "0" + d : d);
};
