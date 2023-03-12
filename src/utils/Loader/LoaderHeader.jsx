import React from "react";
import ContentLoader from "react-content-loader";
import "./loader.scss";
const LoaderHeader = () => {
  return (
    <div className="loader-header">
      <ContentLoader viewBox="0 0 800 60">
        <rect x="12" y="15" rx="6" ry="6" width="155" height="32" />
        <rect x="220" y="20" rx="6" ry="6" width="380" height="25" />
        <rect x="655" y="15" rx="6" ry="6" width="70" height="32" />
        <rect x="750" y="15" rx="10" ry="10" width="35" height="35" />
      </ContentLoader>
    </div>
  );
};

export default LoaderHeader;
