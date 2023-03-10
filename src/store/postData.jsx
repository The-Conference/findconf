import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";
import { dateToYMD } from "../utils/dateSort";
const initialState = {
  filters: {
    searchValue: "",
    filter: {
      online: false,
      offline: false,
      rinc: false,
      register: false,
      nearest: false,
    },
  },
  conferences: [],
  isLoading: false,
  error: false,
};
export const postData = createSlice({
  name: "conferences",
  initialState,
  reducers: {
    startLoading: (state) => {
      state.isLoading = true;
    },
    hasError: (state, action) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    reset: (state) => {
      return (state.conferences = []);
    },

    handleFollow: (state, action) => {
      return state.conferences.forEach((el) =>
        el.id === action.payload ? (el.follow = !el.follow) : el
      );
    },
    handleSave: (state, action) => {
      return window.localStorage.setItem(
        "fave",
        JSON.stringify(action.payload)
      );
    },
    saveFilter: (state, action) => {
      if (action.payload === "онлайн") {
        state.filters.filter.online = !state.filters.filter.online;
      }
      if (action.payload === "оффлайн") {
        state.filters.filter.offline = !state.filters.filter.offline;
      }
      if (action.payload === "ринц") {
        state.filters.filter.rinc = !state.filters.filter.rinc;
      }
      if (action.payload === "идет регистрация") {
        state.filters.filter.register = !state.filters.filter.register;
      }
      if (action.payload === "ближайшие") {
        state.filters.filter.nearest = !state.filters.filter.nearest;
      }
    },
    deleteAllFilters: (state, action) => {
      state.filters.filter = {
        online: false,
        offline: false,
        rinc: false,
        register: false,
        nearest: false,
      };
    },
    fetchConferences: (state, action) => {
      state.conferences = [];

      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      let data = action.payload;
      let month = new Date().getMonth() + 1;
      let day = new Date().getDate();
      for (let item of data) {
        item.follow =
          followed.includes(item.id) && followed.length > 0 ? true : false;
        item.register =
          new Date(item.reg_date_end).getMonth() + 1 < month ||
          (new Date(item.reg_date_end).getMonth() + 1 === month &&
            new Date(item.reg_date_end).getDate() < day)
            ? false
            : true;
        item.finished =
          new Date(item.conf_date_end).getMonth() + 1 < month ||
          (new Date(item.conf_date_end).getMonth() + 1 === month &&
            new Date(item.conf_date_end).getDate() < day)
            ? true
            : false;
      }
      state.conferences = data;
    },
    //отсюда начинается фильтрация!!!
    handleFilter: (state, action) => {
      state.conferences = [];

      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      let data = action.payload;
      let month = new Date().getMonth() + 1;
      let day = new Date().getDate();
      for (let item of data) {
        item.follow =
          followed.includes(item.id) && followed.length > 0 ? true : false;
        item.register =
          new Date(item.reg_date_end).getMonth() + 1 < month ||
          (new Date(item.reg_date_end).getMonth() + 1 === month &&
            new Date(item.reg_date_end).getDate() < day)
            ? false
            : true;
        item.finished =
          new Date(item.conf_date_end).getMonth() + 1 < month ||
          (new Date(item.conf_date_end).getMonth() + 1 === month &&
            new Date(item.conf_date_end).getDate() < day)
            ? true
            : false;
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data;
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter((el) => el.online === true);
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter((el) => el.offline === true);
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.offline === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.offline === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.offline === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter((el) => el.rinc === true);
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter((el) => el.register === true);
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.register === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.register === true && el.offline === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.register === true && el.online === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) =>
            el.register === true && el.online === true && el.offline === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) => el.register === true && el.online === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) =>
            el.register === true && el.offline === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === false
      ) {
        state.conferences = data.filter(
          (el) =>
            el.register === true &&
            el.online === true &&
            el.rinc === true &&
            el.offline === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data.sort((a, b) =>
          dateToYMD(new Date(a.conf_date_begin)) >
          dateToYMD(new Date(b.conf_date_begin)) >
          0
            ? 1
            : -1
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.register === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.rinc === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.offline === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.online === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.online === true && el.offline === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.online === true && el.rinc === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.online === true && el.register === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.rinc === true && el.offline === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.register === true && el.offline === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter((el) => el.register === true && el.rinc === true)
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === false &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter(
            (el) =>
              el.online === true && el.offline === true && el.rinc === true
          )
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter(
            (el) =>
              el.online === true && el.register === true && el.rinc === true
          )
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter(
            (el) =>
              el.register === true && el.offline === true && el.rinc === true
          )
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter(
            (el) =>
              el.online === true &&
              el.offline === true &&
              el.rinc === true &&
              el.register === true
          )
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false &&
        state.filters.filter.register === true &&
        state.filters.filter.nearest === true
      ) {
        state.conferences = data
          .filter(
            (el) =>
              el.online === true && el.offline === true && el.register === true
          )
          .sort((a, b) =>
            dateToYMD(new Date(a.conf_date_begin)) >
            dateToYMD(new Date(b.conf_date_begin)) >
            0
              ? 1
              : -1
          );
      }
      state.isLoading = false;
    },
  },
  //и только здесь она заканчивается!!!
});
export default postData.reducer;
export const {
  handleFollow,
  handleFilter,
  saveFilter,
  handleSave,
  deleteAllFilters,
  fetchConferences,
  startLoading,
  reset,
  hasError,
} = postData.actions;

export const fetchAllConferences = () => async (dispatch) => {
  dispatch(startLoading());

  try {
    await api.get("/api/").then((response) =>
      setTimeout(() => {
        dispatch(fetchConferences(response.data));
      }, 200)
    );
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const fetchFilteredConferences = () => async (dispatch) => {
  dispatch(startLoading());

  try {
    await api.get("/api/").then((response) =>
      setTimeout(() => {
        dispatch(handleFilter(response.data));
      }, 200)
    );
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state;
