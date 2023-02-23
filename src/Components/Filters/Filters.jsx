import React, { useState, useEffect } from "react";
import "./filters.scss";
import { handleNewFilter, newSelectFilter } from "../../store/newFilter";
import {
  handleFlag,
  selectedFilter,
  handleColor,
  handleDeleteColor,
  removeAllFlags,
} from "../../store/filterSlice";
import { handleFilter, reset } from "../../store/postData";
import { useDispatch, useSelector } from "react-redux";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector(selectedFilter);
  const [filter, setFilter] = useState("");

  const handleFill = (name) => {
    setFilter(name);
  };

  return (
    <div className="filter">
      <button
        on
        style={{
          backgroundColor: data.some((el) => el.applied === true)
            ? "#2c60e7"
            : "#0000381A",
          color: data.some((el) => el.applied === true) ? "white" : "#00002E",
        }}
        className="filter__delete-button"
        onClick={() => {
          dispatch(reset());
          dispatch(handleDeleteColor());
          dispatch(removeAllFlags());
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
              <span>&#10008;</span>
              {item.name}
            </div>
          </div>
          {item.flag === true &&
            item.dropdown.map((el) => (
              <label htmlFor="">
                <input
                  type="checkbox"
                  className="filter__container-dropdown"
                  onClick={() => {
                    handleFill(el);
                    // dispatch(handleNewFilter(el));
                    dispatch(handleColor(item.id));
                    dispatch(handleFlag(item.id));
                    dispatch(
                      handleFilter({
                        name: el,
                        id: item.id,
                        org: filter,
                      })
                    );
                  }}
                />
                {el}
              </label>
            ))}
        </div>
      ))}
    </div>
  );
};

export default Filters;
