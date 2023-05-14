import { useEffect } from "react";
import { loginSuccess } from "../../store/authSlice";
import { useDispatch } from "react-redux";

const Profile = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const authToken = localStorage.getItem("authToken");

    if (authToken) {
      dispatch(loginSuccess({ token: authToken }));
    }
  }, [dispatch]);

  return (
    <div>
      <h1>Здесь находится страница авторизованного пользователя </h1>
    </div>
  );
};
export default Profile;
