import { GraduationCap, VideoCamera, Trophy, Group, Coin } from "iconoir-react";
export const sidebar_menu = [
  {
    icon: <GraduationCap width={24} height={24} />,
    text: "Главная",
    link: "/",
  },
  {
    icon: <VideoCamera width={24} height={24} />,
    text: "Конференции",
    link: "/conferences",
  },
  {
    icon: <Trophy width={24} height={24} />,
    text: "Гранты",
    link: "/grants",
  },
  {
    icon: <Group width={24} height={24} />,
    text: "Стажировки",
    link: "/internships",
  },
  {
    icon: <Coin width={24} height={24} />,
    text: "Стипендии",
    link: "/scholarships",
  },
];
