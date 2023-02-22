import axios from "axios";

export const api = axios.create({
  baseURL: "http://django:8000/",
  headers: {
    "Content-Type": "application/json",
  },
});
