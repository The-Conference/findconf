export const removeComma = (obj) => {
  const result = {};
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key];
      result[key] = value.endsWith(",") ? value.slice(0, -1) : value;
    }
  }
  return result;
};
