import { createSlice } from "@reduxjs/toolkit";

export const newFilter = createSlice({
  name: "newfilters",
  initialState: [],
  reducers: {
    handleNewFilter: (state, action) => {
      return (state = [action.payload]);
    },
  },
});

export const { handleNewFilter } = newFilter.actions;
export const newSelectFilter = (state) => state.newfilters;

export default newFilter.reducer;
