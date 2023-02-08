import React from "react";
import { MutatingDots } from "react-loader-spinner";
const Spinner = () => {
  return (
    <MutatingDots
      height="100"
      width="100"
      color="#2c60e7"
      secondaryColor="#00002e"
      radius="10.5"
      ariaLabel="mutating-dots-loading"
      wrapperStyle={{ display: "flex", justifyContent: "center" }}
      wrapperClass=""
      visible={true}
    />
  );
};
export default Spinner;
