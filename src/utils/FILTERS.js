import conferenceCard from "./mock";

const FILTERS = [
  {
    name: "Организатор",
    id: 1,
    flag: false,
    applied: false,
    dropdown: Array.from(new Set(conferenceCard.map((el) => el.organizer))),
  },
  {
    name: "Форма участия",
    id: 2,
    flag: false,
    applied: false,
    dropdown: ["online", "offline"],
  },
  {
    name: "Тематика",
    id: 3,
    flag: false,
    applied: false,
    dropdown: ["архитектура", "строительство", "медицина"],
  },
  {
    name: "Публикация работы",
    id: 4,
    flag: false,
    applied: false,
    dropdown: ["ринц", "винкс"],
  },
  {
    name: "Статус",
    id: 5,
    flag: false,
    applied: false,
    dropdown: [
      "Идет регистрация",
      "Регистрация окончена",
      "Конференция завершена",
    ],
  },
  //   {
  //     name: "Дата",
  //     id: 6,
  //     flag: false,
  //applied: false,
  //     dropdown: [
  //       "Идет регистрация",
  //       "Регистрация окончена",
  //       "Конференция завершена",
  //     ],
  //   },
  {
    name: "Место",
    id: 7,
    flag: false,
    applied: false,
    dropdown: [
      "Идет регистрация",
      "Регистрация окончена",
      "Конференция завершена",
    ],
  },
];

export { FILTERS };

//спросить про парсерсы , как обрабатываются и помешаются в базу данных, этап администрирования (для удаления, редактирования, создания конференций и как это взаимодействет с парсерами), вопрос по фильтрам
