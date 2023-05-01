import axios from "axios";

export const api = axios.create({
  baseURL: "https://theconf.ru/",
  headers: {
    "Content-Type": "application/json",
  },
});
