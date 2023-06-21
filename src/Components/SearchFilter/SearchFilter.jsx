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
    const { value } = event.target;
    const trimmedValue = value.trim().replace(/[+/)/(/*/^/$/-/-/%/|/?/]/gi, "");
    const regex = new RegExp(trimmedValue.split(" ").join("|"), "gi");
    setValue(value);
    const updatedList = search.filter(
      ({ org_name, conf_name, tags }) =>
        regex.test(org_name) ||
        regex.test(conf_name) ||
        tags.some(({ name }) => regex.test(name)) ||
        regex.test("онлайн") ||
        regex.test("офлайн")
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
                          textToHighlight={item.org_name}
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
                        <small>
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
                        {item.tags.map((elem) =>
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
                        )}

                        {item.online === true && (
                          <small>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={lighted}
                              autoEscape={false}
                              textToHighlight={"онлайн"}
                              key={index}
                            />
                          </small>
                        )}
                        {item.offline === true && (
                          <small>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={lighted}
                              autoEscape={false}
                              textToHighlight={"офлайн"}
                              key={index}
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
