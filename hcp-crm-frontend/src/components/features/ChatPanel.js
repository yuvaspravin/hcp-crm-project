import React from "react";
import { Send } from "lucide-react";
import { useChat } from "../../hooks/useChat"; // Import the new hook

const ChatPanel = () => {
  const { messages, input, setInput, isLoading, handleSend } = useChat();

  return (
    <div className="w-1/2 flex flex-col bg-white border-l h-screen">
      <div className="p-4 border-b bg-blue-50 flex items-center shadow-sm">
        <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold mr-3">
          AI
        </div>
        <h2 className="text-lg font-semibold text-gray-800">AI Assistant</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[75%] p-3 rounded-lg text-sm shadow-sm ${msg.role === "user" ? "bg-blue-600 text-white rounded-br-none" : "bg-white border text-gray-800 rounded-bl-none"}`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-lg text-sm text-gray-500 animate-pulse">
              AI is thinking...
            </div>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSend}
        className="p-4 border-t bg-white flex items-center space-x-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe interaction..."
          disabled={isLoading}
          className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 flex items-center justify-center w-12 transition-colors disabled:bg-blue-400"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

export default ChatPanel;
