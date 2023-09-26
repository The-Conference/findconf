import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { fetchId, addDeleteFave } from "../../store/postData";
import { Star } from "iconoir-react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

function FollowButton({ id, favorite }) {
  const isAuthenticated = useSelector((state) => state.auth.token !== null);
  const [localIsFave, setLocalIsFave] = useState(favorite);
  const dispatch = useDispatch();
  const nav = useNavigate();

  const handleButtonClick = () => {
    if (isAuthenticated) {
      dispatch(fetchId(id));
      dispatch(addDeleteFave());
      setLocalIsFave(!localIsFave);
    } else {
      nav("/login");
    }
  };
  let Follow = null;
  const title = localIsFave ? "удалить из избранного" : "добавить в избранное";

  Follow = localIsFave ? (
    <Star
      fill="#f8d448"
      onClick={handleButtonClick}
      title={title}
      height={24}
      color="#f8d448"
      style={{ cursor: "pointer" }}
      width={24}
    />
  ) : (
    <Star
      style={{ cursor: "pointer" }}
      onClick={handleButtonClick}
      title={title}
      height={24}
      width={24}
    />
  );

  return (
    // <img
    //
    //   onClick={handleButtonClick}
    //   src={img}
    //   alt="follow"
    //   width={type === "card" ? "25" : "32"}
    //   height={type === "card" ? "24" : "32"}
    // />

    <>{Follow}</>
  );
}

export default FollowButton;
