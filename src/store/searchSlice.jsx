import { createSlice } from "@reduxjs/toolkit";

export const Search = createSlice({
  name: "search",
  initialState: false,
  reducers: {
    handleSearch: (state) => {
      return (state = true);
    },
  },
});

export const { handleSearch } = Search.actions;
export const search = (state) => state.search;
export default Search.reducer;
