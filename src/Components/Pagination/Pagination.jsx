import React from "react";
import { useDispatch } from "react-redux";
import "./pagination.scss";
const Pagination = ({
  paginate,
  totalConferences,
  currentConference,
  addMore,
}) => {
  const dispatch = useDispatch();

  return (
    <>
      {currentConference.length !== totalConferences && (
        <div className="showmore" onClick={() => dispatch(addMore(10))}>
          Показать еще
        </div>
      )}
    </>
  );
};

export default Pagination;
