import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcpName: "",
  interactionType: "Meeting",
  date: "",
  time: "",
  attendees: "",
  topicsDiscussed: "",
  materialsShared: [],
  samplesDistributed: [],
  sentiment: "Neutral", // Positive, Neutral, Negative
  outcomes: "",
  followUpActions: [],
};

const formSlice = createSlice({
  name: "form",
  initialState,
  reducers: {
    // Completely overwrite the form (used by log_interaction_tool)
    updateEntireForm: (state, action) => {
      return { ...state, ...action.payload };
    },
    // Update specific fields (used by edit_interaction_tool)
    updateSpecificFields: (state, action) => {
      return { ...state, ...action.payload };
    },
    // Manual fallback clear
    clearForm: () => initialState,
  },
});

export const { updateEntireForm, updateSpecificFields, clearForm } =
  formSlice.actions;
export default formSlice.reducer;
