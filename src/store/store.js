import { configureStore } from "@reduxjs/toolkit";
import postReducer from "./postData";
import filterReducer from "./filterSlice";
import searchReducer from "./searchSlice";
import userReducer from "./userSlice";
import authReducer from "./authSlice";

export default configureStore({
  reducer: {
    conferences: postReducer,
    filters: filterReducer,
    search: searchReducer,
    user: userReducer,
    auth: authReducer,
  },
});
