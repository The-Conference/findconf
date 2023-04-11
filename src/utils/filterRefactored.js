import { dateToYMD } from "../utils/dateSort";

function dynamicFilter(state, data) {
  if (
    state.filters.filter.online === false &&
    state.filters.filter.offline === false &&
    state.filters.filter.rinc === false &&
    state.filters.filter.register === false
  ) {
    state.conferences = data;
  }
  //1 filter
  if (state.filters.filter.online === true) {
    state.conferences = data.filter((el) => el.online === true);
  }
  if (state.filters.filter.offline === true) {
    state.conferences = data.filter((el) => el.offline === true);
  }
  if (state.filters.filter.rinc === true) {
    state.conferences = data.filter((el) => el.rinc === true);
  }
  if (state.filters.filter.register === true) {
    state.conferences = data.filter(
      (el) => el.conf_status === "регистрация началась"
    );
  }
  if (state.filters.filter.nearest === true) {
    state.conferences = data
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  // 2 filters
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true
  ) {
    state.conferences = data.filter(
      (el) => el.online === true && el.offline === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.rinc === true
  ) {
    state.conferences = data.filter(
      (el) => el.online === true && el.rinc === true
    );
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true
  ) {
    state.conferences = data.filter(
      (el) => el.offline === true && el.rinc === true
    );
  }
  if (
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) => el.conf_status === "Регистрация Началась" && el.rinc === true
    );
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) => el.conf_status === "Регистрация Началась" && el.offline === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) => el.conf_status === "Регистрация Началась" && el.online === true
    );
  }
  if (
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.register === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.rinc === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.rinc === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.offline === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.online === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  // 3 filters
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true
  ) {
    state.conferences = data.filter(
      (el) => el.online === true && el.offline === true && el.rinc === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) =>
        el.conf_status === "Регистрация Началась" &&
        el.online === true &&
        el.offline === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) =>
        el.conf_status === "Регистрация Началась" &&
        el.online === true &&
        el.rinc === true
    );
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) =>
        el.conf_status === "Регистрация Началась" &&
        el.offline === true &&
        el.rinc === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.online === true && el.offline === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.online === true && el.rinc === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) => el.online === true && el.conf_status === "Регистрация Началась"
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.rinc === true && el.offline === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter((el) => el.register === true && el.offline === true)
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) => el.conf_status === "Регистрация Началась" && el.rinc === true
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  // 4 filters
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true
  ) {
    state.conferences = data.filter(
      (el) =>
        el.conf_status === "Регистрация Началась" &&
        el.online === true &&
        el.rinc === true &&
        el.offline === true
    );
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) => el.online === true && el.offline === true && el.rinc === true
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) =>
          el.online === true &&
          el.conf_status === "Регистрация Началась" &&
          el.rinc === true
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) =>
          el.conf_status === "Регистрация Началась" &&
          el.offline === true &&
          el.rinc === true
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) =>
          el.online === true &&
          el.offline === true &&
          el.conf_status === "Регистрация Началась"
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
  // 5 filters
  if (
    state.filters.filter.online === true &&
    state.filters.filter.offline === true &&
    state.filters.filter.rinc === true &&
    state.filters.filter.register === true &&
    state.filters.filter.nearest === true
  ) {
    state.conferences = data
      .filter(
        (el) =>
          el.online === true &&
          el.offline === true &&
          el.rinc === true &&
          el.conf_status === "Регистрация Началась"
      )
      .sort((a, b) =>
        dateToYMD(new Date(a.conf_date_begin)) >
        dateToYMD(new Date(b.conf_date_begin)) >
        0
          ? 1
          : -1
      )
      .filter((el) => el.conf_status !== "Конференция окончена");
  }
}

export { dynamicFilter };
