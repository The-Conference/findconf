import { createSlice } from "@reduxjs/toolkit";
import { api } from "../api";
import axios from "axios";
const initialState = {
  count: 0,
  page: 1,
  conferences: [],
  params: "",
  oneConference: null,
  isLoading: false,
  error: false,
  id: null,
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
    handlePage: (state, action) => {
      state.page = action.payload;
    },
    fetchParams: (state, action) => {
      state.params = action.payload;
    },
    cleanParams: (state) => {
      const keyToKeep = "search";
      const newObj = Object.keys(state.params).reduce((acc, key) => {
        if (key === keyToKeep) {
          acc[key] = state.params[key];
        }
        return acc;
      }, {});

      if (state.params.hasOwnProperty("search")) {
        state.params = newObj;
      } else {
        state.params = "";
      }
    },

    handleCount: (state, action) => {
      state.count = action.payload;
    },
    reset: (state) => {
      state.conferences = [];
    },

    fetchConferences: (state, action) => {
      state.conferences = state.conferences.concat(action.payload);
      state.isLoading = false;
    },
    fetchConferencesOnce: (state, action) => {
      state.conferences = [];
      state.conferences = action.payload;
      state.isLoading = false;
    },
    fetchId: (state, action) => {
      state.id = action.payload;
    },

    fetchOne: (state, action) => {
      state.oneConference = action.payload;
    },
  },
});
export default postData.reducer;
export const {
  fetchConferences,
  startLoading,
  reset,
  hasError,
  fetchOne,
  fetchParams,
  handlePage,
  handleCount,
  cleanParams,
  fetchId,
  fetchConferencesOnce,
} = postData.actions;

export const fetchOnce = () => async (dispatch) => {
  dispatch(startLoading());
  const Token = localStorage.getItem("auth_token"); // Получение токена из Local Storage

  const headers = {
    Authorization: `Token ${Token}`,
    Accept: "application/json",
  };

  try {
    if (Token) {
      const response = await api.get(`/api/`, {
        headers,
      });
      dispatch(fetchConferencesOnce(response.data.results));
      dispatch(handleCount(response.data.count));
    } else {
      const response = await api.get(`/api/`);
      dispatch(fetchConferencesOnce(response.data.results));
      dispatch(handleCount(response.data.count));
    }
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const fetchFavourite = () => async (dispatch) => {
  dispatch(startLoading());
  const Token = localStorage.getItem("auth_token"); // Получение токена из Local Storage
  const headers = {
    Authorization: `Token ${Token}`,
    Accept: "application/json",
  };

  try {
    if (Token) {
      const response = await api.get(`/api/favorites/`, {
        headers,
      });
      dispatch(fetchConferencesOnce(response.data));
      dispatch(handleCount(response.data.count));
      console.log(response.data);
    }
  } catch (e) {
    dispatch(hasError(e.message));
  }
};

export const filteredContent = () => async (dispatch, getState) => {
  dispatch(startLoading());
  const Token = localStorage.getItem("auth_token"); // Получение токена из Local Storage

  const { page } = getState().conferences;
  const { params } = getState().conferences;

  const urlParams = new URLSearchParams(params);
  const finalUrl = `${urlParams.toString()}`;
  const readyUrl = decodeURI(finalUrl).replace(/%2C/gi, ",");

  const headers = {
    Authorization: `Token ${Token}`,
    Accept: "application/json",
  };

  try {
    if (Token) {
      const response = await api.get(`/api/?${readyUrl}&page=${page}`, {
        headers,
      });
      dispatch(fetchConferences(response.data.results));
      dispatch(handleCount(response.data.count));
    } else {
      const response = await api.get(`/api/?${readyUrl}&page=${page}`);
      dispatch(fetchConferences(response.data.results));
      dispatch(handleCount(response.data.count));
    }
  } catch (e) {
    dispatch(hasError(e.message));
  }
};
export const addDeleteFave = () => async (dispatch, getState) => {
  const accessToken = localStorage.getItem("auth_token"); // Получение токена из Local Storage
  const { id } = getState().conferences;

  if (!accessToken) {
    throw new Error("Токен не найден в Local Storage");
  }

  const headers = {
    Authorization: `Token ${accessToken}`,
    Accept: "application/json",
  };

  try {
    const response = await axios.get(
      `https://test.theconf.ru/api/${id}/favorite/`,
      { headers }
    );

    return response.data; // Возвращает полученные данные из ответа
  } catch (error) {
    throw error; // Обработка ошибок, например, вывод или повторная попытка
  }
};

export const card = (state) => state;
