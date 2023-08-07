import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";
import axios from "axios";
const initialState = {
  count: 0,
  page: 1,
  conferences: [],
  oneConference: null,
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
    handlePage: (state, action) => {
      state.page = action.payload;
    },

    handleCount: (state, action) => {
      state.count = action.payload;
    },
    reset: (state) => {
      state.conferences = [];
    },

    fetchConferences: (state, action) => {
      // state.conferences = [];
      state.conferences = state.conferences.concat(action.payload);
      state.isLoading = false;
    },

    fetchOne: (state, action) => {
      state.oneConference = action.payload;
    },
  },
});
export default postData.reducer;
export const {
  fetchConferences,
  startLoading,
  reset,
  hasError,
  fetchOne,
  handlePage,
  handleCount,
} = postData.actions;

// export const fetchAllConferences = () => async (dispatch) => {
//   dispatch(startLoading());

//   try {
//     const response = await api.get(`/api/`);
//     dispatch(fetchConferences(response.data.results));
//     dispatch(handleCount(response.data.count));
//   } catch (e) {
//     dispatch(hasError(e.message));
//   }
// };
export const addMoreConferences = () => async (dispatch, getState) => {
  dispatch(startLoading());
  const { page } = getState().conferences;
  console.log(page);
  try {
    const response = await axios.get(page);
    dispatch(fetchConferences(response.data.results));
    dispatch(handleCount(response.data.count));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const filteredContent = () => async (dispatch, getState) => {
  dispatch(startLoading());
  const { page } = getState().conferences;
  const currentUrl = window.location.href;
  let query = "?" + currentUrl.split("?")[1];
  let replacedUrl = query.replace(/\+/g, "%20").replace(/%2C/g, ",");
  console.log(page);
  const readyUrl =
    query.includes("true") ||
    query.includes("date_asc") ||
    query.includes("date_desc") ||
    query.includes("undefined")
      ? replacedUrl
      : replacedUrl.slice(0, -1);

  try {
    const response = await api.get(`/api/${readyUrl}&page=${page}`);
    dispatch(fetchConferences(response.data.results));
    dispatch(handleCount(response.data.count));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state;
