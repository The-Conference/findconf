import { configureStore } from "@reduxjs/toolkit";
import postReducer from "./postData";
import filterReducer from "./filterSlice";
import searchReducer from "./searchSlice";

export default configureStore({
  reducer: {
    conferences: postReducer,
    filters: filterReducer,
    search: searchReducer,
  },
});
