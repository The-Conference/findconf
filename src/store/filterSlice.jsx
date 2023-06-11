import { createSlice } from "@reduxjs/toolkit";
import { FILTERS } from "../utils/FILTERS";

export const filterSlice = createSlice({
  name: "filters",
  initialState: FILTERS,
  reducers: {
    handleColor: (state, action) => {
      return state.map((el) =>
        el.id === action.payload ? { ...el, applied: true } : el
      );
    },
    handleDeleteColor: (state, action) => {
      return state.map((el) =>
        el.id === action.payload ? { ...el, applied: false } : el
      );
    },
    handleDeleteAllColors: (state) => {
      state.map((el) => (el.applied = false));
    },
  },
});

export const { handleColor, handleDeleteColor, handleDeleteAllColors } =
  filterSlice.actions;
export const filter = (state) => state.filters;
export const selectedFilter = (state) => state.filters;
export default filterSlice.reducer;
