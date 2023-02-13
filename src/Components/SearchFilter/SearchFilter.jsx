import React from "react";
import { card } from "../../store/postData";
import { useSelector } from "react-redux";
import "./searchfilter.scss";
import search from "./searchgrey.svg";
import Highlighter from "react-highlight-words";
import { useState } from "react";

const SearchFilter = () => {
  const data = useSelector(card);

  const [filteredList, setFilteredList] = useState(data);
  const [value, setValue] = useState("");
  let query = "";
  const filterBySearch = (event) => {
    query = event.target.value;
    setValue(event.target.value);
    var updatedList = [...data];

    updatedList = updatedList.filter((item) => {
      return (
        item.organizer.toLowerCase().indexOf(query.toLowerCase()) !== -1 ||
        item.title.toLowerCase().indexOf(query.toLowerCase()) !== -1
      );
    });

    setFilteredList(updatedList);
  };
  const handleSubmit = (e, val) => {
    e.preventDefault();
    console.log(val);
  };
  return (
    <form className="search" onSubmit={(e) => handleSubmit(e, value)}>
      <div className="input">
        <img src={search} alt="search" />
        <input
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
                  <div className="conf">
                    <li key={index}>
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
                  </div>
                )
            )}
          {filteredList.length > 0 && value.length > 0 && (
            <div className="sticky-button">
              <button>Все результаты</button>
            </div>
          )}
        </ul>
      </div>
    </form>
  );
};
export default SearchFilter;
