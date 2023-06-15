const FILTERS = [
  {
    name: "ВУЗ",
    id: 1,
    applied: false,
    data: [
      "Рабочий и крестьянка",
      "Живущий в облаках",
      "Бегущий за ветром",
      "Не придумал как назвать",
      "Курский институт",
      "Ярославкий институт",
      "Минский институт",
      "Ростовский институт",
      "Белгородский государственный национальный исследовательский университет",
    ].map((item) => ({ name: item, key: "un_name", checked: false })),
  },
  {
    name: "Тематика",
    id: 2,
    applied: false,
    data: [
      "Автоматика",
      "Промышленность",
      "Спорт",
      "Индастриал",
      "Бизнес",
      "Экономика",
      "Развлечения",
      "Машиностроение",
    ].map((item) => ({ name: item, key: "tags", checked: false })),
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
      { name: "РИНЦ", key: "rinc", checked: false },
      { name: "ВАК", key: "vak", checked: false },
      { name: "Scopus", key: "scopus", checked: false },
      { name: "WOS", key: "wos", checked: false },
    ],
  },
  {
    name: "Статус",
    id: 5,
    applied: false,
    data: [
      { name: "Конференция идёт", key: "started", checked: false },
      {
        name: "Конференция скоро начнётся",
        key: "starting_soon",
        checked: false,
      },
      { name: "Конференция окончена", key: "finished", checked: false },
      {
        name: "Неизвестно (уточнить у организатора)",
        key: "unknown",
        checked: false,
      },
    ],
  },

  {
    name: "Форма участия",
    id: 6,
    applied: false,
    data: [
      { name: "Онлайн", key: "online", checked: false },
      { name: "Офлайн", key: "offline", checked: false },
    ],
  },
  {
    name: "Сортировка",
    id: 7,
    applied: false,
    data: ["По дате", "По статусу"].map((item) => ({
      name: item,
      key: "sort",
      checked: false,
    })),
  },
];
const allKeys = [
  { id: 1, keys: ["un_name"] },
  { id: 2, keys: ["tags"] },
  { id: 5, keys: ["started", "finished", "unknown", "starting_soon"] },
  { id: 4, keys: ["rinc", "vak", "scopus", "wos"] },
  { id: 6, keys: ["online", "offline"] },
  { id: 7, keys: ["sort"] },
];
export { FILTERS, allKeys };
