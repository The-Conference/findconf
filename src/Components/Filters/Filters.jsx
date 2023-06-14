import React, { useState, useEffect } from "react";
import "./filters.scss";
import {
  saveFilter,
  fetchFilteredConferences,
  filteredContent,
} from "../../store/postData";
import {
  handleColor,
  handleDeleteColor,
  handleDeleteAllColors,
} from "../../store/filterSlice";
import { useDispatch, useSelector } from "react-redux";
import white from "../../assets/whitecross.svg";
import grey from "../../assets/greycross.svg";
import { allKeys } from "../../utils/FILTERS";
import reset from "../../assets/reset.svg";
import {
  StyledPopup,
  StyledPopupTitle,
  StyledPopupText,
  StyledPopupDiv,
  StyledPopupClose,
  StyledPopupInput,
  StyledScroll,
} from "./styled";
import "reactjs-popup/dist/index.css";
import Fuse from "fuse.js";
import { SearchBar } from "./SearchBar";
import { useSearchParams } from "react-router-dom";

const Filters = () => {
  const dispatch = useDispatch();
  const data = useSelector((state) => state.filters);
  const [dataFiltered, setData] = useState(data);
  const [dataInitial, setDataInitial] = useState(data);
  const [menu, setMenu] = useState(false);
  const [cardId, setCardId] = useState(0);
  const [searchParams, setSearchParams] = useSearchParams();

  const handleAddParams = (q, value, id) => {
    const currentParams = Object.fromEntries(searchParams.entries());
    const currentValue = currentParams[q];

    let newParams;
    if (currentValue) {
      if (currentValue.includes(value)) {
        const newValue = currentValue.trim().replace(value, "");
        if (newValue === "") {
          delete currentParams[q];
          newParams = currentParams;
          dispatch(handleDeleteColor(id));
        } else {
          newParams = { ...currentParams, [q]: newValue };
        }
      } else {
        newParams = { ...currentParams, [q]: `${currentValue} ${value}` };
      }
    } else {
      newParams = { ...currentParams, [q]: value };
    }

    setSearchParams(new URLSearchParams(newParams));
  };

  const searchData = (pattern) => {
    const options = {
      includeScore: true,
      keys: ["name"],
    };
    const fuse = new Fuse(dataFiltered, options);
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

  useEffect(() => {
    const currentParams = Object.fromEntries(searchParams.entries());

    const all = allKeys.filter((item) =>
      item.keys.find((el) => currentParams.hasOwnProperty(el))
    );

    if (all.length > 0) {
      all.forEach((elem) => dispatch(handleColor(elem.id)));
    }
  }, [cardId, dispatch, searchParams]);

  useEffect(() => {
    dispatch(filteredContent());
  }, [dispatch, searchParams]);

  const currentUrl = window.location.href;
  let query = currentUrl.split("?")[1];
  const decodedUrl = decodeURIComponent(query).split("+").join(" ");

  const deletAllFilters = () => {
    setSearchParams();
  };
  const deleteOneGroup = (id) => {
    const currentParams = Object.fromEntries(searchParams.entries());
    let paramsToRemove = allKeys.filter((el) => el.id === id)[0].keys;
    let newParams;
    paramsToRemove.forEach((param) => {
      if (currentParams.hasOwnProperty(param)) {
        console.log(param);
        delete currentParams[param];
        newParams = currentParams;
        dispatch(handleDeleteColor(id));
      }
    });

    setSearchParams(new URLSearchParams(newParams));
  };
  return (
    <>
      <div className="filter">
        {query && (
          <div
            className={
              query
                ? "applied-hover filter__delete-button "
                : "nonapplied-hover filter__delete-button "
            }
            onClick={() => {
              deletAllFilters();
              dispatch(handleDeleteAllColors());
            }}
          >
            {(query && (
              <img
                src={white}
                title="сбросить все фильтры"
                alt="сбросить фильтры"
                width="14"
                height="14"
              />
            )) || (
              <img
                src={grey}
                title="сбросить все фильтры"
                alt="сбросить фильтры"
                width="14"
                height="14"
              />
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
                    setCardId(item.id);
                  }}
                  className={
                    item.applied === true
                      ? "filter__container-button applied-hover"
                      : "filter__container-button nonapplied-hover"
                  }
                  key={item.id}
                >
                  <div>{item.name}</div>
                  <button>
                    <svg
                      width="10"
                      height="6"
                      viewBox={item.applied !== true ? "0 0 10 6" : "0 0 10 5"}
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
            position="bottom left"
          >
            {(close) => (
              <div>
                <StyledPopupTitle>{item.name}</StyledPopupTitle>
                {(item.name === "ВУЗ" || item.name === "Тематика") && (
                  <SearchBar
                    placeholder="Search"
                    onChange={(e) => searchData(e.target.value)}
                  />
                )}
                <StyledPopupClose
                  className="close"
                  onClick={() => {
                    close();
                  }}
                >
                  <img
                    onClick={() => deleteOneGroup(item.id)}
                    src={reset}
                    alt="сброс фильтров"
                    title="сбросить фильтры"
                  />
                  <img src={grey} alt="close" />
                </StyledPopupClose>
                <StyledScroll>
                  {dataFiltered.map((item, n) => (
                    <StyledPopupDiv key={n + 1}>
                      <StyledPopupInput
                        className="custom-checkbox"
                        id={"color" + n}
                        type="checkbox"
                        checked={
                          (cardId === 4 &&
                            decodedUrl.includes(item.key) === true) ||
                          (cardId === 5 &&
                            decodedUrl.includes(item.key) === true) ||
                          (cardId === 6 &&
                            decodedUrl.includes(item.key) === true) ||
                          (cardId !== 4 &&
                            decodedUrl.includes(item.name) === true) ||
                          (cardId !== 5 &&
                            decodedUrl.includes(item.name) === true) ||
                          (cardId !== 6 &&
                            decodedUrl.includes(item.name) === true)
                            ? true
                            : false
                        }
                        onChange={() => {
                          cardId === 4 || cardId === 5 || cardId === 6
                            ? handleAddParams(item.key, "true", cardId)
                            : handleAddParams(item.key, item.name, cardId);
                          // setKey(item.key);
                        }}
                      />
                      <StyledPopupText for={"color" + n}>
                        {item.name}
                      </StyledPopupText>
                    </StyledPopupDiv>
                  ))}
                </StyledScroll>
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
