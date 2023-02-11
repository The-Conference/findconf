import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./CounterSlice";
import postReducer from "./postData";
import filterReducer from "./filterSlice";

export default configureStore({
  reducer: {
    counter: counterReducer,
    postdata: postReducer,
    filters: filterReducer,
  },
});
