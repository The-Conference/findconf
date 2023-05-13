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
import {
  StyledPopup,
  StyledPopupTitle,
  StyledPopupText,
  StyledPopupLabel,
  StyledPopupClose,
} from "./styled";
import "reactjs-popup/dist/index.css";
import Fuse from "fuse.js";
import { SearchBar } from "./SearchBar";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector(selectedFilter);
  const [dataFiltered, setData] = useState(data);
  const [dataInitial, setDataInitial] = useState(data);
  const [menu, setMenu] = useState(false);

  const searchData = (pattern) => {
    const fuse = new Fuse(dataFiltered);
    const result = fuse.search(pattern);
    const matches = [];

    if (!result.length) {
      setData(dataInitial);
    } else {
      result.forEach(({ item }) => {
        matches.push(item);
      });
      setData(matches);
    }
  };

  return (
    <>
      <div className="filter">
        {data.some((el) => el.applied === true) && (
          <div
            className={
              data.some((el) => el.applied === true)
                ? "applied-hover filter__delete-button "
                : "nonapplied-hover filter__delete-button "
            }
            onClick={() => {
              dispatch(handleDeleteColor());
              dispatch(deleteAllFilters());
              dispatch(fetchFilteredConferences());
            }}
          >
            {(data.some((el) => el.applied === true) && (
              <img src={white} alt="удалить фильтры" width="14" height="14" />
            )) || (
              <img src={grey} alt="удалить фильтры" width="14" height="14" />
            )}
          </div>
        )}

        {data.map((item) => (
          <StyledPopup
            trigger={
              <div className="filter__container" key={item.id}>
                <div
                  onClick={() => {
                    setData(item.data);
                    setDataInitial(item.data);
                    dispatch(handleColor(item.id));
                    dispatch(saveFilter(item.name));
                    dispatch(fetchFilteredConferences());
                  }}
                  className={
                    item.applied === true
                      ? "filter__container-button applied-hover"
                      : "filter__container-button nonapplied-hover"
                  }
                  key={item.id}
                >
                  {item.applied === true && (
                    <svg
                      width="10"
                      height="10"
                      viewBox="0 0 10 10"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M9.35329 8.64666C9.54862 8.842 9.54862 9.15869 9.35329 9.35402C9.25595 9.45135 9.12796 9.50067 8.99996 9.50067C8.87195 9.50067 8.74396 9.45202 8.64662 9.35402L4.99995 5.70733L1.35329 9.35402C1.25595 9.45135 1.12795 9.50067 0.999955 9.50067C0.871955 9.50067 0.743955 9.45202 0.646622 9.35402C0.451289 9.15869 0.451289 8.842 0.646622 8.64666L4.29329 5.00002L0.646622 1.35337C0.451289 1.15804 0.451289 0.841345 0.646622 0.646012C0.841955 0.450678 1.15863 0.450678 1.35396 0.646012L5.00063 4.2927L8.64728 0.646012C8.84262 0.450678 9.15929 0.450678 9.35462 0.646012C9.54995 0.841345 9.54995 1.15804 9.35462 1.35337L5.70795 5.00002L9.35329 8.64666Z"
                        fill="white"
                      />
                    </svg>
                  )}

                  <div>{item.name}</div>

                  <button>
                    <svg
                      width="10"
                      height="6"
                      viewBox={item.applied !== true ? "0 0 10 6" : "0 0 10 2"}
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M5.00002 5.75002C4.80802 5.75002 4.61599 5.67705 4.46999 5.53005L0.469994 1.53005C0.176994 1.23705 0.176994 0.762018 0.469994 0.469018C0.762994 0.176018 1.23803 0.176018 1.53103 0.469018L5.001 3.93899L8.47097 0.469018C8.76397 0.176018 9.23901 0.176018 9.53201 0.469018C9.82501 0.762018 9.82501 1.23705 9.53201 1.53005L5.53201 5.53005C5.38401 5.67705 5.19202 5.75002 5.00002 5.75002Z"
                        fill={item.applied !== true ? "#00002E" : "white"}
                      />
                    </svg>
                  </button>
                </div>
              </div>
            }
            position="bottom center"
          >
            {(close) => (
              <div>
                <StyledPopupTitle>{item.name}</StyledPopupTitle>
                {(item.name === "Организатор" || item.name === "Тематика") && (
                  <SearchBar
                    placeholder="Search"
                    onChange={(e) => searchData(e.target.value)}
                  />
                )}
                <StyledPopupClose
                  className="close"
                  onClick={() => {
                    dispatch(handleDeleteColor());
                    dispatch(deleteAllFilters());
                    dispatch(fetchFilteredConferences());
                    close();
                  }}
                >
                  X
                </StyledPopupClose>
                {dataFiltered.map((item, n) => (
                  <StyledPopupLabel key={n + 1}>
                    <input type="checkbox" />
                    <StyledPopupText>{item}</StyledPopupText>
                  </StyledPopupLabel>
                ))}
              </div>
            )}
          </StyledPopup>
        ))}
      </div>

      <div className="filter-adaptive">
        {data.some((el) => el.applied === true) && (
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
        )}

        <div className="filter-adaptive__container-button">
          <span
            onClick={() => setMenu(!menu)}
            className={
              data.some((el) => el.applied === true)
                ? "filter__delete-button applied-hover"
                : "filter__delete-button nonapplied-hover"
            }
          >
            Фильтры
          </span>
          <ul>
            {menu &&
              data.map((item) => (
                <li
                  className={
                    item.applied === true ? "applied-hover" : "nonapplied-hover"
                  }
                  onClick={() => {
                    dispatch(handleColor(item.id));
                    dispatch(saveFilter(item.name));
                    dispatch(fetchFilteredConferences());
                    setMenu(!menu);
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
