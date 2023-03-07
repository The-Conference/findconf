import React, { useState } from "react";
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
import white from "../../assets/whitecross.svg";
import grey from "../../assets/greycross.svg";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector(selectedFilter);
  const [menu, setMenu] = useState(false);
  return (
    <>
      <div className="filter">
        <button
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
              onClick={() => {
                dispatch(handleColor(item.id));
                dispatch(saveFilter(item.name));
                dispatch(fetchFilteredConferences());
              }}
              className="filter__container-button"
              style={{
                backgroundColor:
                  item.applied === true ? "#2c60e7" : "#0000381A",
                color: item.applied === true ? "white" : "#00002E",
              }}
              key={item.id}
            >
              <div>{item.name}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="filter-adaptive">
        <button
          style={{
            backgroundColor: data.some((el) => el.applied === true)
              ? "#2c60e7"
              : "#0000381A",
          }}
          className="filter-adaptive__delete-button"
          onClick={() => {
            dispatch(handleDeleteColor());
            dispatch(deleteAllFilters());
            dispatch(fetchFilteredConferences());
            setMenu(false);
          }}
        >
          {(data.some((el) => el.applied === true) && (
            <img src={white} alt="" />
          )) || <img src={grey} alt="" />}
        </button>
        <div className="filter-adaptive__container-button">
          <span
            onClick={() => setMenu(!menu)}
            style={{
              backgroundColor: data.some((item) => item.applied === true)
                ? "#2c60e7"
                : "#0000381A",
              color: data.some((item) => item.applied === true)
                ? "white"
                : "#00002E",
            }}
          >
            Фильтры
          </span>
          <ul>
            {menu &&
              data.map((item) => (
                <li
                  onClick={() => {
                    dispatch(handleColor(item.id));
                    dispatch(saveFilter(item.name));
                    dispatch(fetchFilteredConferences());
                    setMenu(!menu);
                  }}
                  style={{
                    backgroundColor:
                      item.applied === true ? "#2c60e7" : "#0000381A",
                    color: item.applied === true ? "white" : "#00002E",
                  }}
                  key={item.id}
                >
                  <div>{item.name}</div>
                </li>
              ))}
          </ul>
        </div>
      </div>
    </>
  );
};

export default Filters;
