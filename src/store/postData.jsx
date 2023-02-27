import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";

const initialState = {
  filters: {
    searchValue: "",
    filter: { online: false, offline: false, rinc: false },
  },
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
      state.conferences = [];
      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];

      action.payload.forEach((item) => {
        state.conferences.push({
          address: item.conf_address,
          link: item.conf_card_href,
          description: item.conf_desc,
          online: item.online ? "онлайн" : "",
          offline: item.offline ? "оффлайн" : "",
          local: item.local,
          title: item.conf_name,
          id: item.id,
          follow:
            followed.includes(item.id) && followed.length > 0 ? true : false,
          regStart: item.reg_date_begin,
          regEnd: item.reg_date_end,
          contacts: item.contacts,
          organizer: item.org_name,
          dateStart: item.conf_date_begin,
          dateEnd: item.conf_date_end,
          tags: item.themes.split(","),
          rinc: item.rinc ? "ринц" : "без публикации",
          reg: item.reg_href,
        });
      });
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
    saveFilter: (state, action) => {
      if (action.payload === "онлайн") {
        state.filters.filter.online = !state.filters.filter.online;
      }
      if (action.payload === "оффлайн") {
        state.filters.filter.offline = !state.filters.filter.offline;
      }
      if (action.payload === "ринц") {
        state.filters.filter.rinc = !state.filters.filter.rinc;
      }
    },
    deleteAllFilters: (state, action) => {
      state.filters.filter = { online: false, offline: false, rinc: false };
    },
    handleFilter: (state, action) => {
      state.conferences = [];
      let followed = JSON.parse(window.localStorage.getItem("fave")) || [];
      console.log(action.payload);
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false
      ) {
        action.payload.forEach((item) =>
          state.conferences.push({
            address: item.conf_address,
            link: item.conf_card_href,
            description: item.conf_desc,
            online: item.online ? "онлайн" : "",
            offline: item.offline ? "оффлайн" : "",
            local: item.local,
            title: item.conf_name,
            id: item.id,
            follow:
              followed.includes(item.id) && followed.length > 0 ? true : false,
            regStart: item.reg_date_begin,
            regEnd: item.reg_date_end,
            contacts: item.contacts,
            organizer: item.org_name,
            dateStart: item.conf_date_begin,
            dateEnd: item.conf_date_end,
            tags: item.themes.split(","),
            rinc: item.rinc ? "ринц" : "",
            reg: item.reg_href,
          })
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === false
      ) {
        action.payload.filter((item) =>
          item.online === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false
      ) {
        action.payload.forEach((item) =>
          item.offline === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === false
      ) {
        action.payload.forEach((item) =>
          item.online === true && item.offline === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true
      ) {
        action.payload.forEach((item) =>
          item.online === true && item.offline === true && item.rinc === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc === true ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === true &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true
      ) {
        action.payload.filter((item) =>
          item.online === true && item.offline === false && item.rinc === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === true &&
        state.filters.filter.rinc === true
      ) {
        action.payload.filter((item) =>
          item.online === false && item.offline === true && item.rinc === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
      if (
        state.filters.filter.online === false &&
        state.filters.filter.offline === false &&
        state.filters.filter.rinc === true
      ) {
        action.payload.filter((item) =>
          item.rinc === true
            ? state.conferences.push({
                address: item.conf_address,
                link: item.conf_card_href,
                description: item.conf_desc,
                online: item.online ? "онлайн" : "",
                offline: item.offline ? "оффлайн" : "",
                local: item.local,
                title: item.conf_name,
                id: item.id,
                follow:
                  followed.includes(item.id) && followed.length > 0
                    ? true
                    : false,
                regStart: item.reg_date_begin,
                regEnd: item.reg_date_end,
                contacts: item.contacts,
                organizer: item.org_name,
                dateStart: item.conf_date_begin,
                dateEnd: item.conf_date_end,
                tags: item.themes.split(","),
                rinc: item.rinc ? "ринц" : "",
                reg: item.reg_href,
              })
            : []
        );
      }
    },
  },
});
export default postData.reducer;
export const {
  handleFollow,
  handleFilter,
  saveFilter,
  handleSave,
  deleteAllFilters,
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
export const fetchFilteredConferences = () => async (dispatch) => {
  dispatch(startLoading());
  try {
    await api
      .get("/api/")
      .then((response) => dispatch(handleFilter(response.data)));
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const card = (state) => state;
// state.filters.filter.includes(action.payload)
//   ? state.filters.filter.splice(
//       state.filters.filter.indexOf(action.payload),
//       1
//     )
//   : state.filters.filter.push(action.payload);
