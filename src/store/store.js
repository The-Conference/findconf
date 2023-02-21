import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./CounterSlice";
import postReducer from "./postData";
import filterReducer from "./filterSlice";
import searchReducer from "./searchSlice";
import newFilterReducer from "./newFilter";

export default configureStore({
  reducer: {
    counter: counterReducer,
    conferences: postReducer,
    filters: filterReducer,
    search: searchReducer,
    newfilters: newFilterReducer,
  },
});
