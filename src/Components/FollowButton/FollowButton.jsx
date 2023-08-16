import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { fetchId, addDeleteFave } from "../../store/postData";
import hearts from "../../assets/follow.svg";
import following from "../../assets/following.svg";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import hearts2 from "../../assets/followSmall.svg";
import following2 from "../../assets/followingSmall.svg";
function FollowButton({ id, favorite, type }) {
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
  let img = null;
  if (type === "card") {
    img = localIsFave ? following : hearts;
  } else {
    img = localIsFave ? following2 : hearts2;
  }

  const title = localIsFave ? "удалить из избранного" : "добавить в избранное";

  return (
    <img
      title={title}
      onClick={handleButtonClick}
      src={img}
      alt="follow"
      width={type === "card" ? "25" : "32"}
      height={type === "card" ? "24" : "32"}
    />
  );
}

export default FollowButton;
