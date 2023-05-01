import { render, screen } from "@testing-library/react";
import AboutService from "./AboutService";

describe("AboutService", () => {
  test("About snapshot", () => {
    const view = render(<AboutService />);
    expect(view).toMatchSnapshot();
  });
  test("styles checked", () => {
    render(<AboutService />);
    expect(
      screen.getByText(
        "Сервис был запущен в 2023 году с целью упрощения поиска конференций для студентов различных направлений и профессионалов своего дела"
      )
    ).toHaveClass("about__launched");
  });
});
