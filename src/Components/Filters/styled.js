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

export const StyledPopupText = styled.p`
  font-size: 14px;
  margin-left: 10px;
`;

export const StyledPopupLabel = styled.label`
  display: flex;
  margin-bottom: 10px;
`;

export const StyledPopupClose = styled.p`
  position: absolute;
  top: 14px;
  right: 12px;
  padding: 5px;
  cursor: pointer;
`;

export const StyledSearchInput= styled.input`
border: 1px solid #4834e8;
border-radius: 5px;
margin-bottom: 10px;
width: 100%;
`;
