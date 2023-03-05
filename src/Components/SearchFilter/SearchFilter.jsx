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
  const [popup, setPopup] = useState(false);
  useOnClickOutside(ref, () => setPopup(false));
  let query = "";

  const filterBySearch = (event) => {
    query = event.target.value;

    setValue(
      event.target.value.replace(
        /[+/)/(/*/^/$/|/%/]/gi,
        " characterREPLACEMENT"
      )
    );

    var updatedList = [...search];
    updatedList = updatedList.filter((item) => {
      return (
        item.org_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.conf_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.themes.toLowerCase().indexOf(query.toLowerCase()) !== -1
      );
    });
    setFilteredList(updatedList);
    if (value.length > 0) {
      setPopup(true);
    }
  };

  const handleKeyDown = (event) => {
    if (value.length !== 0) {
      if (event.key === "Enter") {
        nav(`/search/${value}`);
      }
    }
  };

  useEffect(() => {
    window.scrollTo(0, 0);
    dispatch(fetchResults());
  }, []);
  return (
    <form className="search" onKeyDown={handleKeyDown}>
      <div className="input">
        <input
          autoFocus={true}
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
          {value.length !== 0 &&
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
                          searchWords={[value]}
                          autoEscape={true}
                          textToHighlight={item.org_name}
                        />
                      </li>
                      <div>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={[value]}
                          autoEscape={true}
                          textToHighlight={item.conf_name}
                        />
                      </div>
                      <div>
                        {item.themes.split(",").map((tag, index) => (
                          <small key={index}>
                            <Highlighter
                              highlightClassName="highlight"
                              searchWords={[value]}
                              autoEscape={true}
                              textToHighlight={tag}
                            />
                          </small>
                        ))}
                      </div>
                    </div>
                  </Link>
                )
            )}
          {filteredList.length > 0 && value.length > 0 && popup === true && (
            <div className="sticky-button">
              <a href={`/search/${value}`}>
                <button onClick={() => setValue("")}>Все результаты</button>
              </a>
            </div>
          )}
        </ul>
      </div>
    </form>
  );
};
export default SearchFilter;
