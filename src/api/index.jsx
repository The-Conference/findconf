import axios from "axios";
const API_URL = "https://test.theconf.ru/";
export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
