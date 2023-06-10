const FILTERS = [
  {
    name: "ВУЗ",
    id: 1,
    applied: false,
    key: "un_name",
    data: [
      "Рабочий и крестьянка",
      "Живущий в облаках",
      "Бегущий за ветром",
      "Не придумал как назвать",
      "Курский институт",
      "Ярославкий институт",
      "Минский институт",
      "Ростовский институт",
    ],
  },
  {
    name: "Тематика",
    id: 2,
    applied: false,
    key: "tags",
    data: [
      "Автоматика",
      "Промышленность",
      "Спорт",
      "Индастриал",
      "Бизнес",
      "Экономика",
      "Развлечения",
      "Машиностроение",
    ],
  },
  {
    name: "Город",
    id: 3,
    applied: false,
    key: "city",
    data: ["Москва", "Питер", "Ростов", "Челябинск"],
  },

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
      { name: "Конференция скоро начнётся", key: "starting_soon" },
      { name: "Конференция окончена", key: "finished" },
      { name: "Неизвестно (уточнить у организатора)", key: "unknown" },
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
    key: "sort",
    data: ["По дате", "По статусу"],
  },
];

export { FILTERS };
