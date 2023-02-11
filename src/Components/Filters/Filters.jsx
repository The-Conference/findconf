import React from "react";
import "./filters.scss";
import {
  handleFlag,
  selectedFilter,
  handleColor,
  handleDeleteColor,
} from "../../store/filterSlice";
import { handleFilter, handleDelete } from "../../store/postData";
import { useDispatch, useSelector } from "react-redux";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector(selectedFilter);

  return (
    <div className="filter">
      <button
        style={{
          backgroundColor: data.some((el) => el.applied === true)
            ? "#2c60e7"
            : "#0000381A",
          color: data.some((el) => el.applied === true) ? "white" : "#00002E",
        }}
        className="filter__delete-button"
        onClick={() => {
          dispatch(handleDelete());
          dispatch(handleDeleteColor());
        }}
      >
        X
      </button>
      {data.map((item) => (
        <div className="filter__container">
          <div
            className="filter__container-button"
            style={{
              backgroundColor: item.applied === true ? "#2c60e7" : "#0000381A",
              color: item.applied === true ? "white" : "#00002E",
            }}
            key={item.id}
          >
            <div onClick={() => dispatch(handleFlag(item.id))}>
              {" "}
              <span>&#10008;</span>
              {item.name}
            </div>
          </div>
          {item.flag === true &&
            item.dropdown.map((el) => (
              <div
                className="filter__container-dropdown"
                onClick={() => {
                  dispatch(handleFilter({ name: el, id: item.id }));
                  dispatch(handleColor(item.id));
                  dispatch(handleFlag(item.id));
                }}
              >
                {el}
              </div>
            ))}
        </div>
      ))}
    </div>
  );
};

export default Filters;
