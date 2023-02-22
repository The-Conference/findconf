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
            organizer: item.un_name,
            dateStart: item.conf_date_begin,
            dateEnd: item.conf_date_end,
            tags: item.themes,
            rinc: item.rinc,
          });
        });
      }
    },
    // conf_address
    // :
    // "Место проведения конгресса : ПСПбГМУ им. И.П. Павлова аудитория №1 и конференц-зале корпуса №54 , онлайн-трансляция"
    // conf_card_href
    // :
    // "https://www.1spbgmu.ru/nauka/konferentsii/nauka/konferentsii/6998-31-marta-1-aprelya-sostoitsya-mezhregionalnoj-nauchno-prakticheskoj-konferentsii-nevrologov-sankt-peterburga-i-severo-zapadnogo-federalnogo-okruga-rf-khkhi-severnaya-shkola"
    // conf_date_begin
    // :
    // "2023-04-01"
    // conf_date_end
    // :
    // ""
    // conf_desc
    // :
    // " Глубокоуважаемые коллеги! Приглашаем Вас принять участие в работе Межрегиональной научно-практической конференции неврологов Санкт-Петербурга и Северо-Западного федерального округа РФ (ХХI Северная Школа) , которая состоится 31 марта-1 апреля 2023 года в Санкт-Петербурге.  Формат проведения конгресса : очный с онлайн-трансляцией Открытие конференции : 31 марта 2023 года в 09:00 Место проведения конгресса : ПСПбГМУ им. И.П. Павлова аудитория №1 и конференц-зале корпуса №54 , онлайн-трансляция  Организаторы: Основные темы:  ЗАЯВКИ НА ДОКЛАДЫ просим высылать профессору Амелину Александру Витальевичу avamelin@mail.ru и ассистенту кафедры Пономареву Григорию Вячеславовичу grigoryponomarev@yandex.ru до 20 февраля 2023 года. Регламент выступления соответствует 15 минутам. ИНФОРМАЦИОННОЕ ПИСЬМО"
    // conf_href
    // :
    // "отсутствует"
    // conf_id
    // :
    // "1spbgmu_6998-31-marta-1-aprelya-sostoitsya-mezhregionalnoj-nauchno-prakticheskoj-konferentsii-nevrologov-sankt-peterburga-i-severo-zapadnogo-federalnogo-okruga-rf-khkhi-severnaya-shkola"
    // conf_name
    // :
    // "31 марта - 1 апреля состоится Межрегиональной научно-практической конференции неврологов Санкт-Петербурга и Северо-Западного федерального округа РФ (ХХI Северная Школа)"
    // conf_s_desc
    // :
    // "Приглашаем Вас принять участие в работе Межрегиональной научно-практической конференции неврологов Санкт-Петербурга и Северо-Западного федерального округа РФ (ХХI Северная Школа) , которая состоится 31 марта-1 апреля 2023 года в Санкт-Петербурге."
    // contacts
    // :
    // "ЗАЯВКИ НА ДОКЛАДЫ просим высылать профессору Амелину Александру Витальевичу avamelin@mail.ru и ассистенту кафедры Пономареву Григорию Вячеславовичу grigoryponomarev@yandex.ru до 20 февраля 2023 года. Регламент выступления соответствует 15 минутам. avamelin@mail.ru grigoryponomarev@yandex.ru"
    // hash
    // :
    // "f28b1366fe28351c8d52eb48cdc44957"
    // local
    // :
    // true
    // offline
    // :
    // true
    // online
    // :
    // true
    // org_name
    // :
    // "Организаторы:"
    // reg_date_begin
    // :
    // "2023-04-01"
    // reg_date_end
    // :
    // ""
    // reg_href
    // :
    // ""
    // rinc
    // :
    // false
    // themes
    // :
    // ""
    // un_name
    // :
    // "Первый Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова"

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
