import ReactGA from "react-ga";

export const GAListener = ({ children }) => {
  ReactGA.pageview(window.location.pathname + window.location.search);
  return children;
};
