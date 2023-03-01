import React, { useState } from "react";
import { useSelector } from "react-redux";
import "./searchfilter.scss";
import Highlighter from "react-highlight-words";
import { Link, useNavigate } from "react-router-dom";

const SearchFilter = () => {
  const nav = useNavigate();
  const { conferences } = useSelector((state) => state.conferences);
  const [filteredList, setFilteredList] = useState(conferences);
  const [value, setValue] = useState("");

  let query = "";

  const filterBySearch = (event) => {
    query = event.target.value;
    setValue(event.target.value);
    var updatedList = [...conferences];
    updatedList = updatedList.filter((item) => {
      return (
        item.org_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.conf_name.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.themes.toLowerCase().indexOf(query.toLowerCase()) !== -1
      );
    });
    setFilteredList(updatedList);
  };

  const handleKeyDown = (event) => {
    if (value.length !== 0) {
      if (event.key === "Enter") {
        nav(`/search/${value}`);
      }
    }
  };

  return (
    <form className="search" onKeyDown={handleKeyDown}>
      <div className="input">
        <input
          type="search"
          placeholder="Тема конференции, организатор"
          className="search-box"
          onChange={(e) => filterBySearch(e)}
        />
      </div>
      <div className="dropdown-filter">
        <ul>
          {value.length !== 0 &&
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
          {filteredList.length > 0 && value.length > 0 && (
            <div className="sticky-button">
              <Link to={`/search/${value}`}>
                <button onClick={() => setValue("")}>Все результаты</button>
              </Link>
            </div>
          )}
        </ul>
      </div>
    </form>
  );
};
export default SearchFilter;
