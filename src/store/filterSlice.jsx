import { createSlice } from "@reduxjs/toolkit";
import { FILTERS } from "../utils/FILTERS";

export const filterSlice = createSlice({
  name: "filters",
  initialState: FILTERS,
  reducers: {
    handleFlag: (state, action) => {
      return state.map((el) =>
        el.id === action.payload ? { ...el, flag: !el.flag } : el
      );
    },
    handleColor: (state, action) => {
      return state.map((el) =>
        el.id === action.payload ? { ...el, applied: true } : el
      );
    },
    handleDeleteColor: (state) => {
      return state.forEach((el) => (el.applied = false));
    },
  },
});

export const { handleFlag, handleColor, handleDeleteColor } =
  filterSlice.actions;
export const filter = (state) => state.filters;
export const selectedFilter = (state) => state.filters;
export default filterSlice.reducer;
