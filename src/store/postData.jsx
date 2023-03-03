import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

const initialState = {
  filters: {
    searchValue: "",
    filter: { online: false, offline: false, rinc: false },
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

    fetchConferences: (state, action) => {
      state.conferences = [];
      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      let data = action.payload;
      for (let item of data) {
        item.follow =
          followed.includes(item.id) && followed.length > 0 ? true : false;
      }
      state.conferences = data;
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
    },
    deleteAllFilters: (state, action) => {
      state.filters.filter = { online: false, offline: false, rinc: false };
    },
    handleFilter: (state, action) => {
      state.conferences = [];

      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      let data = action.payload;
      for (let item of data) {
        item.follow =
          followed.includes(item.id) && followed.length > 0 ? true : false;
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false
      ) {
        state.conferences = data;
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false
      ) {
        state.conferences = data.filter((el) => el.online === true);
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false
      ) {
        state.conferences = data.filter((el) => el.offline === true);
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.offline === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.offline === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true
      ) {
        state.conferences = data.filter(
          (el) => el.online === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true
      ) {
        state.conferences = data.filter(
          (el) => el.offline === true && el.rinc === true
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true
      ) {
        state.conferences = data.filter((el) => el.rinc === true);
      }
      state.isLoading = false;
    },
  },
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
    await api
      .get("/api/")
      .then((response) => dispatch(fetchConferences(response.data)));
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
      }, 1000)
    );
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state;
