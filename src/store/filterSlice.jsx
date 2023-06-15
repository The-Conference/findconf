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
    handleData: (state, action) => {
      return state.map((el) =>
        el.id === action.payload.id ? { ...el, data: action.payload.data } : el
      );
    },
  },
});

export const {
  handleColor,
  handleDeleteColor,
  handleDeleteAllColors,
  handleData,
} = filterSlice.actions;
export const filter = (state) => state.filters;
export const selectedFilter = (state) => state.filters;
export default filterSlice.reducer;
