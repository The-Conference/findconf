import React, { useEffect } from "react";
import "./conference.scss";
import { useSelector, useDispatch } from "react-redux";
import LoaderTemplate from "../../utils/Loader/LoaderTemplate";
import { LoaderTemplateTwo } from "../../utils/Loader/LoaderTemplate";
import {
  filteredContent,
  handlePage,
  fetchFavourite,
} from "../../store/postData";
import Filters from "../Filters/Filters";
import EmptyResult from "../EmptyResult/EmptyResult";
import EmptyFave from "../EmptyResult/emptyFave";
import Title from "./Title";
import Card from "./Card";
const AllConferences = ({ data, keywords, id }) => {
  const { conferences, isLoading, count, page } = useSelector(
    (state) => state.conferences
  );
  let result = [];
  let recsPrev = [];

  // const { value } = useSelector((state) => state.search);
  const dispatch = useDispatch();

  useEffect(() => {
    if (data === "favourites") {
      dispatch(fetchFavourite());
    }
  }, [dispatch, data]);

  useEffect(() => {
    if (
      conferences.length < count &&
      data !== "prev" &&
      data !== "prev4" &&
      data !== "favorites"
    ) {
      const fetchData = async () => {
        try {
          dispatch(handlePage(page + 1));
          dispatch(filteredContent());
        } catch (error) {
          console.log(error);
        }
      };
      const handleScroll = () => {
        const scrollHeight = document.documentElement.scrollHeight;
        const scrollTop = document.documentElement.scrollTop;
        const clientHeight = document.documentElement.clientHeight;

        // проверяем, достигли ли мы конца скролла
        if (scrollTop + clientHeight + 100 >= scrollHeight && !isLoading) {
          fetchData();
        }
      };

      window.addEventListener("scroll", handleScroll);
      return () => {
        window.removeEventListener("scroll", handleScroll);
      };
    }
  }, [dispatch, isLoading, page, count, conferences.length, data]);

  if (data === "prev4") {
    let newValue = keywords
      .trim()
      .split(" ")
      .filter((el) => el.length > 2)
      .join("|");

    let regexp = new RegExp(newValue, "gi");
    recsPrev = conferences.filter((el) => {
      return (
        regexp.test(el.title) || regexp.test(el.tags.map((item) => item.name))
      );
    });
  }

  const types = {
    prev4: recsPrev.filter((el) => el.id !== id).slice(0, 2),
  };

  if (data === "prev4") {
    result = types.prev4;
  } else {
    result = conferences;
  }

  return (
    <section className={data === "prev4" ? "conf-prev prev" : "conference"}>
      <Title data={data} />
      {data !== "prev" && data !== "prev4" && data !== "favourites" && (
        <Filters />
      )}
      {(isLoading && data !== "prev" && data !== "prev4" && (
        <LoaderTemplate />
      )) ||
        (isLoading && <LoaderTemplateTwo />)}
      {!isLoading &&
        result.length === 0 &&
        data !== "favourites" &&
        data !== "prev" &&
        data !== "prev4" && <EmptyResult />}
      {!isLoading && result.length === 0 && data === "favourites" && (
        <EmptyFave />
      )}
      <div className="conference__container">
        {result.length > 0 && result.map((el) => <Card el={el} />)}
      </div>
      {isLoading && (
        <div style={{ marginTop: "50px" }}>
          <LoaderTemplateTwo />
        </div>
      )}
    </section>
  );
};

export default AllConferences;
