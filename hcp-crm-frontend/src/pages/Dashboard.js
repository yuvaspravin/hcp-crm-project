import React from "react";
import FormPanel from "../components/features/FormPanel";
import ChatPanel from "../components/features/ChatPanel";

const Dashboard = () => {
  return (
    <div className="flex w-full h-screen overflow-hidden font-sans text-gray-900 bg-white">
      <FormPanel />
      <ChatPanel />
    </div>
  );
};

export default Dashboard;
