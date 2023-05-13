import React from "react";
import { StyledSearchInput } from "./styled";

export const SearchBar = ({ onChange }) => {
  return (
    <>
      <StyledSearchInput type="text" onChange={onChange} />
    </>
  );
};
