import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

const initialState = {
  count: 0,
  page: 1,
  conferences: [],
  params: "",
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
    fetchParams: (state, action) => {
      state.params = action.payload;
    },
    cleanParams: (state, action) => {
      state.params = "";
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
  fetchParams,
  handlePage,
  handleCount,
  cleanParams,
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

export const filteredContent = () => async (dispatch, getState) => {
  dispatch(startLoading());
  const { page } = getState().conferences;
  const { params } = getState().conferences;

  // Формирование URL-строки с параметрами
  const urlParams = new URLSearchParams(params);
  const finalUrl = `${urlParams.toString()}`;
  const readyUrl = decodeURI(finalUrl).replace(/%2C/gi, ",");

  try {
    const response = await api.get(`/api/?${readyUrl}&page=${page}`);
    dispatch(fetchConferences(response.data.results));
    dispatch(handleCount(response.data.count));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state;
