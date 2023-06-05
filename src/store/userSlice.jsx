import axios from "axios";
import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice({
  name: "user",
  initialState: {
    loading: false,
    error: null,
    currentUser: null,
    registered: false,
  },
  reducers: {
    registerStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    registerSuccess: (state, action) => {
      state.loading = false;
      state.currentUser = action.payload;
      state.registered = true;
    },
    registerFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const { registerStart, registerSuccess, registerFailure } =
  userSlice.actions;

export const registerUser = (userData) => async (dispatch) => {
  dispatch(registerStart());

  try {
    const response = await axios.post(
      "https://test.theconf.ru/api/auth/users/",
      userData
    );
    dispatch(registerSuccess(response.data));
    console.log(response.data);
  } catch (error) {
    dispatch(registerFailure(error.message));
    console.log(error.message);
  }
};

export default userSlice.reducer;
//"http://localhost:3000/signup"
