import React from "react";
import { useSelector } from "react-redux";
import "./searchfilter.scss";
import Highlighter from "react-highlight-words";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import divider from "./Divider.svg";

const SearchFilter = () => {
  const { conferences } = useSelector((state) => state.conferences);
  const nav = useNavigate();
  const [filteredList, setFilteredList] = useState(conferences);
  const [value, setValue] = useState("");

  let query = "";
  const filterBySearch = (event) => {
    query = event.target.value;
    setValue(event.target.value);
    var updatedList = [...conferences];

    updatedList = updatedList.filter((item) => {
      return (
        item.organizer.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.title.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.tags.toLowerCase().indexOf(query.toLowerCase()) !== -1
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
                          textToHighlight={item.organizer}
                        />
                      </li>
                      <div>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={[value]}
                          autoEscape={true}
                          textToHighlight={item.title}
                        />
                      </div>
                      <small>
                        <Highlighter
                          highlightClassName="highlight"
                          searchWords={[value]}
                          autoEscape={true}
                          textToHighlight={item.tags.split(",").join("  |  ")}
                        />
                      </small>
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
