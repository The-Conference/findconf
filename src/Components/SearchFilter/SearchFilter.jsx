import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import "./searchfilter.scss";
import Highlighter from "react-highlight-words";
import { Link, useNavigate } from "react-router-dom";
import { fetchResults } from "../../store/searchSlice";
import useOnClickOutside from "../Hooks/useOnClickOutside";
import { options } from "../../utils/options";
const SearchFilter = () => {
  const nav = useNavigate();
  const ref = useRef();
  const dispatch = useDispatch();
  const { search } = useSelector((state) => state);

  const [filteredList, setFilteredList] = useState(search);
  const [value, setValue] = useState("");
  const [focus, setFocus] = useState(false);
  let lighted = value
    .trim()
    .split(" ")
    .filter((el) => el.length > 2);

  const handleValue = (e) => {
    e.preventDefault();

    handleNavigation();
  };
  const [popup, setPopup] = useState(false);
  useOnClickOutside(ref, () => setPopup(false));

  const filterBySearch = (event) => {
    let newValue = event.target.value
      .trim()
      .replace(/[+/)/(/*/^/$/-/-/%/|/?/]/gi, "")
      .split(" ")
      .join("|");
    let regexp = new RegExp(newValue, "gi");
    setValue(event.target.value);

    var updatedList = [...search];
    updatedList = updatedList.filter((item) => {
      return (
        regexp.test(item.org_name) ||
        regexp.test(item.conf_name) ||
        regexp.test(item.themes) ||
        regexp.test("онлайн") ||
        regexp.test("офлайн")
      );
    });
    setFilteredList(updatedList);
    if (value.length > 0) {
      setPopup(true);
    }
  };
  const handleNavigation = () => {
    if (value.length > 1) {
      nav({ pathname: "/search", search: `?q=${value}` });
      window.location.reload();
    }
  };
  const handleFocus = () => {
    dispatch(fetchResults());
    setFocus(true);
  };
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <form
      className="search"
      onSubmit={(e) => handleValue(e)}
      style={{ border: focus ? "2px solid #4074fb" : "none" }}
    >
      <div className="input">
        <input
          onFocus={handleFocus}
          onBlur={() => setFocus(false)}
          maxLength={100}
          type="search"
          placeholder="Тема конференции, организатор, тематика"
          className={focus === true ? "input-focused" : "search-box"}
          onChange={(e) => {
            filterBySearch(e);
          }}
        />
      </div>
      <div className="dropdown-filter" ref={ref}>
        <ul>
          {lighted.length !== 0 &&
            popup === true &&
            filteredList.map(
              (item, index) =>
                index < 3 && (
                  <Link
                    key={item.id}
                    to={`/conferences/${item.id}`}
                    onClick={() => setValue("")}
                  >
                    <div className="conf">
                      <li>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={lighted}
                          autoEscape={false}
                          textToHighlight={item.org_name}
                        />
                      </li>
                      <div>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={lighted}
                          autoEscape={false}
                          textToHighlight={item.conf_name}
                        />
                      </div>
                      <div>
                        <small>
                          <Highlighter
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
                        {item.themes.split(",").map((tag, index) => (
                          <small key={index}>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={lighted}
                              autoEscape={false}
                              textToHighlight={tag}
                            />
                          </small>
                        ))}
                        {item.online === true && (
                          <small key={index}>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={lighted}
                              autoEscape={false}
                              textToHighlight={"онлайн"}
                            />
                          </small>
                        )}
                        {item.offline === true && (
                          <small key={index}>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={lighted}
                              autoEscape={false}
                              textToHighlight={"офлайн"}
                            />
                          </small>
                        )}
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
                Все результаты
              </button>
            </div>
          )}
        </ul>
      </div>
    </form>
  );
};
export default SearchFilter;
