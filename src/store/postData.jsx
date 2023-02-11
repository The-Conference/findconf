import { createSlice } from "@reduxjs/toolkit";
import conferenceCard from "../utils/mock";

export const postData = createSlice({
  name: "postdata",
  initialState: conferenceCard,
  reducers: {
    handleFollow: (state, action) => {
      return state.map((el) =>
        el.id === action.payload ? { ...el, follow: !el.follow } : el
      );
    },
    handleFilter: (state, action) => {
      return action.payload.id === 1
        ? state.filter((el) => el.organizer === action.payload.name)
        : action.payload.id === 2
        ? state.filter((el) => el.form.includes(action.payload.name))
        : action.payload.id === 3
        ? state.filter((el) => el.themes.includes(action.payload.name))
        : action.payload.id === 4
        ? state.filter((el) => el.publish.includes(action.payload.name))
        : action.payload.id === 5
        ? state.filter((el) =>
            action.payload.name === "Идет регистрация"
              ? el.register === true
              : action.payload.name === "Регистрация окончена"
              ? el.register === false && el.finished === false
              : action.payload.name === "Конференция завершена"
              ? el.finished === true
              : "none"
          )
        : state;
    },
    handleDelete: (state) => {
      return (state = conferenceCard);
    },
  },
});

export const { handleFollow, handleFilter, handleDelete } = postData.actions;
export const card = (state) => state.postdata;
export default postData.reducer;
