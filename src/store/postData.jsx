import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

const initialState = {
  conferences: [],
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
    fetchConferences: (state, action) => {
      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      if (state.conferences.length === 0) {
        action.payload.forEach((item) => {
          state.conferences.push({
            address: item.conf_address,
            link: item.conf_card_href,
            description: item.conf_desc,
            online: item.online,
            offline: item.offline,
            local: item.local,
            title: item.conf_name,
            id: item.hash,
            follow:
              followed.includes(item.hash) && followed.length > 0
                ? true
                : false,
            regStart: item.reg_date_begin,
            regEnd: item.reg_date_end,
            contacts: item.contacts,
            organizer: item.org_name,
            dateStart: item.conf_date_begin,
            dateEnd: item.conf_date_end,
            tags: item.themes,
            rinc: item.rinc,
            reg: item.reg_href,
          });
        });
      }
    },
    handleFollow: (state, action) => {
      return state.conferences.forEach((el) =>
        el.id === action.payload ? (el.follow = !el.follow) : el
      );
    },
    handleSave: (state, action) => {
      return window.localStorage.setItem(
        "fave",
        JSON.stringify(action.payload)
      );
    },
    handleFilter: (state, action) => {
      return state.conferences.filter((el) =>
        action.payload.org.includes(el.organizer)
      );
    },
  },
});
export default postData.reducer;
export const {
  handleFollow,
  handleFilter,
  handleSave,
  fetchConferences,
  startLoading,
  reset,
  hasError,
} = postData.actions;
export const fetchAllConferences = () => async (dispatch) => {
  dispatch(startLoading());
  try {
    await api
      .get("/api/")
      .then((response) => dispatch(fetchConferences(response.data)));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state.conferences;
