const FILTERS = [
  {
    name: "ВУЗ",
    id: 1,
    applied: false,
    data: [],
  },
  {
    name: "Тематика",
    id: 2,
    applied: false,
    data: [],
  },
  // {
  //   name: "Город",
  //   id: 3,
  //   applied: false,
  //   key: "city",
  //   data: ["Москва", "Питер", "Ростов", "Челябинск"],
  // },

  {
    name: "Публикация",
    id: 4,
    applied: false,
    data: [
      { name: "РИНЦ", key: "rinc" },
      { name: "ВАК", key: "vak" },
      { name: "Scopus", key: "scopus" },
      { name: "WOS", key: "wos" },
    ],
  },
  {
    name: "Статус",
    id: 5,
    applied: false,
    data: [
      { name: "Конференция идёт", key: "conf_status", query: "started" },
      {
        name: "Конференция скоро начнётся",
        key: "conf_status",
        query: "starting_soon",
      },
      { name: "Конференция окончена", key: "conf_status", query: "finished" },
      {
        name: "Неизвестно (уточнить у организатора)",
        key: "conf_status",
        query: "unknown",
      },
    ],
  },

  {
    name: "Форма участия",
    id: 6,
    applied: false,
    data: [
      { name: "Онлайн", key: "online" },
      { name: "Офлайн", key: "offline" },
    ],
  },
  {
    name: "Сортировка",
    id: 7,
    applied: false,
    data: [
      {
        name: "По возрастанию",
        key: "ordering",
        query: "date_asc",
      },
      {
        name: "По убыванию",
        key: "ordering",
        query: "date_desc",
      },
    ],
  },
];
const allKeys = [
  { id: 1, keys: ["un_name"] },
  { id: 2, keys: ["tags"] },
  { id: 5, keys: ["conf_status"] },
  { id: 4, keys: ["rinc", "vak", "scopus", "wos"] },
  { id: 6, keys: ["online", "offline"] },
  { id: 7, keys: ["ordering"] },
];
export { FILTERS, allKeys };
