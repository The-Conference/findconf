import React from "react";
import ContentLoader from "react-content-loader";
import "./loader.scss";
const LoaderHeader = () => {
  return (
    <div className="loader">
      <ContentLoader viewBox="0 0 800 60">
        <rect x="170" y="10" rx="6" ry="6" width="355" height="32" />
        <rect x="570" y="10" rx="6" ry="6" width="120" height="32" />
        <rect x="750" y="10" rx="50" ry="50" width="35" height="35" />
      </ContentLoader>
    </div>
  );
};

export default LoaderHeader;
