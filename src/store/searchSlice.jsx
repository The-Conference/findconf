import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

export const Search = createSlice({
  name: "search",
  initialState: {
    universities: [],
    tags: [],
    search: [],
    value: "",
  },
  reducers: {
    handleUnis: (state, action) => {
      state.universities = action.payload;
    },
    handleTags: (state, action) => {
      state.tags = action.payload;
    },
    handleSearch: (state, action) => {
      state.search = action.payload;
    },
    getValue: (state, action) => {
      state.value = action.payload;
    },
  },
});

export const { handleUnis, handleTags, handleSearch, getValue } =
  Search.actions;
export const search = (state) => state.search;
export const fetchUnis = () => async (dispatch) => {
  try {
    await api
      .get("/api/lists/universities/")
      .then((response) => dispatch(handleUnis(response.data)));
  } catch (e) {
    console.log(e);
  }
};
export const fetchTags = () => async (dispatch) => {
  try {
    await api
      .get("/api/lists/tags/")
      .then((response) => dispatch(handleTags(response.data)));
  } catch (e) {
    console.log(e);
  }
};
export const SearchResults = () => async (dispatch, getState) => {
  const { value } = getState().search;

  try {
    await api
      .get(`/api/?search=${value}`)
      .then((response) => dispatch(handleSearch(response.data.results)));
  } catch (e) {
    console.log(e);
  }
};
export default Search.reducer;
