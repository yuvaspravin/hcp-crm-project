import axios from "axios";

// This URL will point to your FastAPI server later
const API_BASE_URL = "http://localhost:8000";

export const chatService = {
  sendMessage: async (message, currentFormState) => {
    try {
      // In Phase 2, this will send the user's message AND the Redux state to FastAPI
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        formState: currentFormState,
      });
      return response.data;
    } catch (error) {
      console.error("Error communicating with AI Backend:", error);
      throw error;
    }
  },
};
