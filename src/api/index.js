import axios from "axios";

export const api = axios.create({
<<<<<<< HEAD
  baseURL: "https://theconf.ru/",
=======
  baseURL: "https://test.theconf.ru/",
>>>>>>> frontend
  headers: {
    "Content-Type": "application/json",
  },
});
