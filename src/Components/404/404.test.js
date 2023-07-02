import React from "react";
import { shallow } from "enzyme";
import NotFound from "./404";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import Enzyme from "enzyme";

Enzyme.configure({ adapter: new Adapter() });

describe("NotFound component", () => {
  it("renders without crashing", () => {
    shallow(<NotFound />);
  });

  it("displays the heading text correctly", () => {
    const wrapper = shallow(<NotFound />);
    const heading = wrapper.find("h1");
    expect(heading.text()).toEqual("Что-то пошло не так(");
  });

  it("displays the paragraph text correctly", () => {
    const wrapper = shallow(<NotFound />);
    const para = wrapper.find("p");
    expect(para.text()).toEqual("Не волнуйся, мы уже работаем над ошибкой)");
  });

  it("displays the button text correctly", () => {
    const wrapper = shallow(<NotFound />);
    const button = wrapper.find("button");
    expect(button.text()).toEqual("Вернуться домой");
  });

  it("navigates to home page when button is clicked", () => {
    const wrapper = shallow(<NotFound />);
    const button = wrapper.find("button");
    button.simulate("click", { button: 0 });
    expect(window.location.pathname).toEqual("/");
  });
});
