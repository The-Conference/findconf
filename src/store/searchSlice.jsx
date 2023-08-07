import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

export const Search = createSlice({
  name: "search",
  initialState: [],
  reducers: {
    handleSearch: (state, action) => {
      return (state = action.payload);
    },
  },
});

export const { handleSearch } = Search.actions;
export const search = (state) => state.search;
export const fetchResults = () => async (dispatch) => {
  try {
    await api
      .get("/api/")
      .then((response) => dispatch(handleSearch(response.data.results)));
  } catch (e) {
    console.log(e);
  }
};
export default Search.reducer;
