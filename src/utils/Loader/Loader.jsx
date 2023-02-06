import React from "react";
import ContentLoader from "react-content-loader";
import "./loader.scss";
const Loader = () => {
  return (
    <div className="loader">
      <ContentLoader viewBox="0 0 700 180">
        {/* Only SVG shapes */}
        <rect x="20" y="0" rx="15" ry="15" width="650" height="100" />
        <rect x="20" y="110" rx="15" ry="15" width="650" height="50" />
      </ContentLoader>
      <ContentLoader viewBox="0 0 700 180">
        {/* Only SVG shapes */}
        <rect x="20" y="0" rx="15" ry="15" width="650" height="100" />
        <rect x="20" y="110" rx="15" ry="15" width="650" height="50" />
      </ContentLoader>
    </div>
  );
};

export default Loader;
