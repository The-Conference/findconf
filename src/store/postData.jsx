import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

const initialState = {
  conferences: [],
  query: "",
  filters: {
    form: "",
    status: "",
    publish: "",
    city: "",
    themes: "",
    schools: "",
    sort: "",
  },
  isLoading: false,
  error: false,
  currentPage: 1,
  conferencesPerPage: 20,
};
export const postData = createSlice({
  name: "conferences",
  initialState,
  reducers: {
    startLoading: (state) => {
      state.isLoading = true;
    },
    addMore: (state, action) => {
      state.conferencesPerPage = state.conferencesPerPage + action.payload;
    },
    paginate: (state, action) => {
      state.currentPage = action.payload;
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

    // saveFilter: (state, action) => {
    //   if (action.payload === "онлайн") {
    //     state.filters.filter.online = !state.filters.filter.online;
    //   }
    //   if (action.payload === "оффлайн") {
    //     state.filters.filter.offline = !state.filters.filter.offline;
    //   }
    //   if (action.payload === "ринц") {
    //     state.filters.filter.rinc = !state.filters.filter.rinc;
    //   }
    //   if (action.payload === "регистрация началась") {
    //     state.filters.filter.register = !state.filters.filter.register;
    //   }
    //   if (action.payload === "ближайшие") {
    //     state.filters.filter.nearest = !state.filters.filter.nearest;
    //   }
    // },
    // deleteAllFilters: (state, action) => {
    //   state.filters.filter = {
    //     online: false,
    //     offline: false,
    //     rinc: false,
    //     register: false,
    //     nearest: false,
    //   };
    // },
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

    handleFilter: (state, action) => {
      state.conferences = [];

      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      let data = action.payload;

      for (let item of data) {
        item.follow =
          followed.includes(item.id) && followed.length > 0 ? true : false;
      }
      state.conferences = data;
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
  paginate,
  addMore,
  parseUrl,
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
  dispatch(paginate(1));

  try {
    await api
      .get(`/api/`)
      .then((response) => dispatch(handleFilter(response.data)));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const filteredContent = () => async (dispatch) => {
  dispatch(startLoading());
  dispatch(paginate(1));
  const currentUrl = window.location.href;
  let query = "?" + currentUrl.split("?")[1];
  let replacedUrl = query.replace(/\+/g, "%20").replace(/%2C/g, ",");

  const readyUrl = query.includes("true")
    ? replacedUrl
    : replacedUrl.slice(0, -1);
  // console.log(readyUrl);
  try {
    await api.get(`/api/${readyUrl}`).then((response) => {
      dispatch(handleFilter(response.data));
      // console.log(response.data);
    });
  } catch (e) {
    dispatch(hasError(e.message));
  }
};
export const card = (state) => state;
