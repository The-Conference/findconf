import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { fetchId, addDeleteFave } from "../../store/postData";
import hearts from "../../assets/follow.svg";
import following from "../../assets/following.svg";
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

  const img = localIsFave ? following : hearts;
  const title = localIsFave ? "удалить из избранного" : "добавить в избранное";

  return (
    <img
      title={title}
      onClick={handleButtonClick}
      src={img}
      alt="follow"
      width="25"
      height="24"
    />
  );
}

export default FollowButton;
