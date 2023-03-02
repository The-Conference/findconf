import axios from "axios";

export const api = axios.create({
  baseURL: "http://51.250.91.147:8000/",
  headers: {
    "Content-Type": "application/json",
  },
});
