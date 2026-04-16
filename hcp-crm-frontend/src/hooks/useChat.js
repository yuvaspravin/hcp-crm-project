import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { chatService } from "../services/api";
import { updateEntireForm } from "../redux/formSlice";

export const useChat = () => {
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "Hello! I am your AI Assistant. Describe your interaction, and I will log the details for you.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // 1. Grab the current form data and the dispatch function from Redux
  const currentFormState = useSelector((state) => state.form);
  const dispatch = useDispatch();

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add User Message to UI instantly
    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // 2. Send the message AND the current form state to FastAPI
      const response = await chatService.sendMessage(input, currentFormState);

      // 3. Add the AI's text response to the chat
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: response.ai_message },
      ]);

      // 4. If the AI sent back updated form data, update the left panel!
      if (response.updated_form_state) {
        dispatch(updateEntireForm(response.updated_form_state));
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Error: Could not connect to the FastAPI backend.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, input, setInput, isLoading, handleSend };
};
