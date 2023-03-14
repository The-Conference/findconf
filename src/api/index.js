import axios from "axios";

export const api = axios.create({
  baseURL: "https://test.theconf.ru:8000/",
  headers: {
    "Content-Type": "application/json",
  },
});
