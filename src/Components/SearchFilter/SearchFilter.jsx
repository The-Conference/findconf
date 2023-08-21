import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import "./searchfilter.scss";
import Highlighter from "react-highlight-words";
import { Link, useNavigate } from "react-router-dom";
import { SearchResults, getValue } from "../../store/searchSlice";
import useOnClickOutside from "../Hooks/useOnClickOutside";
import { options } from "../../utils/options";
import { useSearchParams } from "react-router-dom";

const SearchFilter = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const nav = useNavigate();
  const ref = useRef();
  const [popup, setPopup] = useState(false);
  useOnClickOutside(ref, () => setPopup(false));
  const dispatch = useDispatch();
  const { search } = useSelector((state) => state.search);

  const [filteredList, setFilteredList] = useState(search);

  const [value, setValue] = useState("");
  const [focus, setFocus] = useState(false);
  let lighted = value
    .trim()
    .split(" ")
    .filter((el) => el.length > 2);
  const handleInputChange = (e) => {
    setSearchParams({ search: e.target.value });
  };

  const handleValue = (e) => {
    e.preventDefault();

    handleNavigation();
  };

  const filterBySearch = (event) => {
    const { value } = event.target;
    const trimmedValue = value.trim().replace(/[+/)/(/*/^/$/-/-/%/|/?/]/gi, "");
    const regex = new RegExp(trimmedValue.split(" ").join("|"), "gi");
    setValue(value);
    const updatedList = search.filter(
      ({ un_name, conf_name, tags }) =>
        regex.test(un_name) || regex.test(conf_name)
      //  ||
      // tags.some(({ name }) => regex.test(name))
      //  ||
      // regex.test("онлайн") ||
      // regex.test("офлайн")
    );
    setFilteredList(updatedList);
    if (value.length > 0) {
      setPopup(true);
    }
  };
  const handleNavigation = () => {
    if (value.length > 1) {
      nav({ pathname: "/search", search: `?search=${value}` });
      window.location.reload();
    }
  };

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  useEffect(() => {
    dispatch(getValue(searchParams.get("search")));
    dispatch(SearchResults());
  }, [searchParams, dispatch]);
  return (
    <form className="search" onSubmit={(e) => handleValue(e)}>
      {focus === true ? <div className="focus"></div> : null}
      <div className="input">
        <input
          onFocus={() => {
            setFocus(true);
          }}
          onBlur={() => {
            setFocus(false);
          }}
          maxLength={100}
          type="search"
          placeholder="Тема конференции, организатор, тематика"
          className={focus === true ? "input-focused" : "search-box"}
          value={searchParams.get("search") || ""}
          onChange={(e) => {
            handleInputChange(e);

            filterBySearch(e);
          }}
        />
        <button onClick={handleNavigation}>Найти</button>
      </div>
      <div className="dropdown-filter" ref={ref}>
        <ul>
          {lighted.length !== 0 &&
            popup === true &&
            filteredList.map(
              (item, index) =>
                index < 3 && (
                  <Link
                    key={index}
                    to={`/conferences/${item.id}`}
                    onClick={() => setValue("")}
                  >
                    <div className="conf" key={index}>
                      <li>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={lighted}
                          autoEscape={false}
                          textToHighlight={item.un_name}
                          key={index}
                        />
                      </li>
                      <div>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={lighted}
                          autoEscape={false}
                          textToHighlight={item.conf_name}
                          key={index}
                        />
                      </div>
                      <div>
                        <small className="tags-date">
                          <Highlighter
                            key={index}
                            highlightClassName="highlight"
                            searchWords={lighted}
                            autoEscape={false}
                            textToHighlight={
                              item.conf_date_end === null
                                ? new Date(item.conf_date_begin)
                                    .toLocaleDateString("ru", options)
                                    .slice(0, -3)
                                : item.conf_date_begin === null
                                ? new Date(item.conf_date_end)
                                    .toLocaleDateString("ru", options)
                                    .slice(0, -3)
                                : item.conf_date_end !== item.conf_date_begin
                                ? new Date(item.conf_date_begin)
                                    .toLocaleDateString("ru", options)
                                    .slice(0, -3) +
                                  " - " +
                                  new Date(item.conf_date_end)
                                    .toLocaleDateString("ru", options)
                                    .slice(0, -3)
                                : new Date(item.conf_date_begin)
                                    .toLocaleDateString("ru", options)
                                    .slice(0, -3)
                            }
                          />
                        </small>
                        {/* {item.tags.map((elem) =>
                          elem.name.split(",").map((tag, index) => (
                            <small>
                              <Highlighter
                                highlightClassName="highlight"
                                searchWords={lighted}
                                autoEscape={false}
                                textToHighlight={tag}
                                key={index}
                              />
                            </small>
                          ))
                        )} */}
                      </div>
                    </div>
                  </Link>
                )
            )}
          {filteredList.length > 0 && lighted.length > 0 && popup === true && (
            <div className="sticky-button">
              <button
                onClick={() => {
                  handleNavigation();
                  setValue("");
                }}
              >
                Показать все результаты
              </button>
            </div>
          )}
        </ul>
      </div>
    </form>
  );
};
export default SearchFilter;
