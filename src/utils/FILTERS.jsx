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
      { name: "Конференция идёт", key: "started" },
      {
        name: "Конференция скоро начнётся",
        key: "starting_soon",
      },
      { name: "Конференция окончена", key: "finished" },
      {
        name: "Неизвестно (уточнить у организатора)",
        key: "unknown",
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
        query: "conf_date_begin",
      },
      {
        name: "По убыванию",
        key: "ordering",
        query: "-conf_date_begin",
      },
    ],
  },
];
const allKeys = [
  { id: 1, keys: ["un_name"] },
  { id: 2, keys: ["tags"] },
  { id: 5, keys: ["started", "finished", "unknown", "starting_soon"] },
  { id: 4, keys: ["rinc", "vak", "scopus", "wos"] },
  { id: 6, keys: ["online", "offline"] },
  { id: 7, keys: ["ordering"] },
];
export { FILTERS, allKeys };
