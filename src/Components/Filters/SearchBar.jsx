import React from "react";
import { StyledSearchInput } from "./styled";

export const SearchBar = ({ onChange, placeholder }) => {
  return (
    <>
      <StyledSearchInput type="text" onChange={onChange} />
    </>
  );
};
