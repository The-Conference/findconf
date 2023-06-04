import axios from "axios";

export const api = axios.create({
  baseURL: "https://test.theconf.ru/",
  headers: {
    "Content-Type": "application/json",
  },
});
