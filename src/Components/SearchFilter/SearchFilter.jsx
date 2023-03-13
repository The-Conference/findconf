import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import "./searchfilter.scss";
import Highlighter from "react-highlight-words";
import { Link, useNavigate } from "react-router-dom";
import { fetchResults } from "../../store/searchSlice";
import useOnClickOutside from "../Hooks/useOnClickOutside";

const SearchFilter = () => {
  const nav = useNavigate();
  const ref = useRef();
  const dispatch = useDispatch();
  const { search } = useSelector((state) => state);
  const [filteredList, setFilteredList] = useState(search);
  const [value, setValue] = useState("");

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
        regexp.test(item.themes)

        // item.org_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        // item.conf_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        // item.themes.toLowerCase().indexOf(query.toLowerCase()) !== -1
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

  useEffect(() => {
    window.scrollTo(0, 0);
    dispatch(fetchResults());
  }, [dispatch]);

  return (
    <form className="search" onSubmit={(e) => handleValue(e)}>
      <div className="input">
        <input
          maxLength={100}
          type="search"
          placeholder="Тема конференции, организатор, тематика"
          className="search-box"
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
