import React, { useState } from "react";

import { useDispatch } from "react-redux";

import "./pagination.scss";
const Pagination = ({ conferencesPerPage, totalConferences, paginate }) => {
  const [active, setActive] = useState(1);
  const dispatch = useDispatch();
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalConferences / conferencesPerPage); i++) {
    pageNumbers.push(i);
  }
  return (
    <div className="pagination">
      <ul>
        {pageNumbers.map((el) => (
          <li
            className={el === active ? "active" : null}
            key={el}
            onClick={() => {
              dispatch(paginate(el));
              setActive(el);
            }}
          >
            {el}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Pagination;
