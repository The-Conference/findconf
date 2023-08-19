import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

export const Search = createSlice({
  name: "search",
  initialState: {
    universities: [],
    tags: [],
  },
  reducers: {
    handleUnis: (state, action) => {
      state.universities = action.payload;
    },
    handleTags: (state, action) => {
      state.tags = action.payload;
    },
  },
});

export const { handleUnis, handleTags } = Search.actions;
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
export default Search.reducer;
