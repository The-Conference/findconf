import React from "react";
import "./filters.scss";

import {
  selectedFilter,
  handleColor,
  handleDeleteColor,
} from "../../store/filterSlice";
import {
  saveFilter,
  deleteAllFilters,
  fetchFilteredConferences,
} from "../../store/postData";
import { useDispatch, useSelector } from "react-redux";
import white from "./whitecross.svg";
import grey from "./greycross.svg";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector(selectedFilter);

  return (
    <div className="filter">
      <button
        on
        style={{
          backgroundColor: data.some((el) => el.applied === true)
            ? "#2c60e7"
            : "#0000381A",
        }}
        className="filter__delete-button"
        onClick={() => {
          dispatch(handleDeleteColor());
          dispatch(deleteAllFilters());
          dispatch(fetchFilteredConferences());
        }}
      >
        {(data.some((el) => el.applied === true) && (
          <img src={white} alt="" />
        )) || <img src={grey} alt="" />}
      </button>
      {data.map((item) => (
        <div className="filter__container" key={item.id}>
          <div
            className="filter__container-button"
            style={{
              backgroundColor: item.applied === true ? "#2c60e7" : "#0000381A",
              color: item.applied === true ? "white" : "#00002E",
            }}
            key={item.id}
          >
            <div
              onClick={() => {
                dispatch(handleColor(item.id));
                dispatch(saveFilter(item.name));
                dispatch(fetchFilteredConferences());
              }}
            >
              {item.name}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Filters;
