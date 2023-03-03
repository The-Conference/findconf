import React from "react";
import ContentLoader from "react-content-loader";
import "./loader.scss";
const Loader = () => {
  return (
    <div className="loader">
      <div>
        <ContentLoader viewBox="0 0 600 380">
          <rect x="20" y="15" rx="6" ry="6" width="155" height="22" />
          <rect x="20" y="175" rx="6" ry="6" width="226" height="22" />
          <rect x="20" y="240" rx="6" ry="6" width="31" height="10" />
          <rect x="60" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="75" y="240" rx="6" ry="6" width="48" height="10" />
          <rect x="133" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="149" y="240" rx="6" ry="6" width="47" height="10" />
          <rect x="210" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="230" y="240" rx="6" ry="6" width="177" height="10" />
          <rect x="20" y="260" rx="16" ry="16" width="550" height="90" />
        </ContentLoader>
      </div>
      <div>
        <ContentLoader viewBox="0 0 600 380">
          <rect x="20" y="15" rx="6" ry="6" width="155" height="22" />
          <rect x="20" y="175" rx="6" ry="6" width="226" height="22" />
          <rect x="20" y="240" rx="6" ry="6" width="31" height="10" />
          <rect x="60" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="75" y="240" rx="6" ry="6" width="48" height="10" />
          <rect x="133" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="149" y="240" rx="6" ry="6" width="47" height="10" />
          <rect x="210" y="242.5" rx="6" ry="6" width="6" height="6" />
          <rect x="230" y="240" rx="6" ry="6" width="177" height="10" />
          <rect x="20" y="260" rx="16" ry="16" width="550" height="90" />
        </ContentLoader>
      </div>
    </div>
  );
};

export default Loader;
