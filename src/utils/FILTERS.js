const FILTERS = [
  {
    name: "Организатор",
    id: 1,
    applied: false,
    data: "bitch",
  },
  {
    name: "Тематика",
    id: 2,
    applied: false,
    data: "bitch",
  },
  {
    name: "Город",
    id: 3,
    applied: false,
    data: "bitch",
  },
  {
    name: "Публикация",
    id: 4,
    applied: false,
    data: ["РИНЦ", "ВАК", "Scopus", "WOS"],
  },
  {
    name: "Статус",
    id: 5,
    applied: false,
    data: [
      "Ожидается регистрация",
      "Регистрация скоро начнётся",
      "Регистрация началась",
      "Регистрация идёт",
      "Регистрация окончена",
      "Конференция запланирована",
      "Конференция скоро начнётся",
      "Конференция идёт",
      "Конференция приостановлена",
      "Конференция окончена",
    ],
  },
  {
    name: "Форма участия",
    id: 6,
    applied: false,
    data: ["Онлайн", "Офлайн"],
  },
  {
    name: "Сортировка",
    id: 7,
    applied: false,
    data: ["По дате", "По статусу"],
  },
];

export { FILTERS };
