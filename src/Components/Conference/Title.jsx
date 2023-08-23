import React from "react";

const Title = ({ data, value }) => {
  return (
    <>
      {data !== "prev" ? (
        <div className="conference__type">
          <div className="back">
            <a href={data !== "prev4" ? "/" : null}>
              <span className="backarrow">&lt;</span>{" "}
              <p>
                {data === "all"
                  ? "Конференции"
                  : data === "favourites"
                  ? "Избранное"
                  : data === "search-results"
                  ? `Результаты по запросу ${value}`
                  : data === "prev4"
                  ? "Похожие конференции"
                  : null}
              </p>
            </a>
          </div>
        </div>
      ) : null}
    </>
  );
};
export default Title;
