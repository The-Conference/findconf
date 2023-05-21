import styled from "styled-components";
import Popup from "reactjs-popup";

export const StyledPopup = styled(Popup)`
  // use your custom style for ".popup-overlay"
  &-overlay {
  }
  // use your custom style for ".popup-content"
  &-content {
    padding: 15px;
    width: 287px !important;
  }
`;

export const StyledPopupTitle = styled.p`
  font-weight: 600;
  font-size: 22px;
  border-bottom: 1px solid #0000381a;
  padding-bottom: 5px;
  margin-bottom: 10px;
`;

export const StyledPopupText = styled.label`
  font-size: 14px;
  display: flex;
  padding: 10px 0;
  &:hover {
    color: #4834e8;
  }
`;

export const StyledPopupDiv = styled.div`
  display: flex;
  &:hover {
    background: rgba(0, 0, 56, 0.1);
    padding: 0px 15px;
    margin-left: -15px;
    margin-right: -15px;
  }
`;

export const StyledPopupClose = styled.p`
  position: absolute;
  top: 14px;
  right: 12px;
  padding: 5px;
  cursor: pointer;
`;

export const StyledSearchInput = styled.input`
  border: 2px solid #4834e8;
  border-radius: 5px;
  margin-bottom: 10px;
  width: 100%;
`;

export const StyledPopupInput = styled.input`
  position: absolute;
  z-index: -1;
  opacity: 0;
  &:label {
    display: inline-flex;
    align-items: center;
    user-select: none;
    margin: 5px 0;
    padding: 5px 0;
  }
  & + label::before {
    content: "";
    display: inline-block;
    width: 19px;
    height: 19px;
    border: 2px solid #00002e;
    border-radius: 5px;
    margin-right: 10px;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 50% 50%;
  }
  &:checked + label::before {
    border-color: #0b76ef;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='blue' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26 2.974 7.25 8 2.193z'/%3e%3c/svg%3e");
  }
  &:not(:disabled):not(:checked) + label:hover::before {
    border-color: #2c60e7;
  }
`;
